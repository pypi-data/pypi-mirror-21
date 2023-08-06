# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.forms.utils import ErrorDict
from django.utils.translation import ugettext_lazy as _
from shop.app_settings import GUEST_IS_ACTIVE_USER
from shop.modifiers.pool import cart_modifiers_pool

from shopit.forms.account import AccountDetailsForm, CleanEmailMixin
from shopit.models.address import ISO_3166_CODES, BillingAddress, ShippingAddress
from shopit.models.cart import CartDiscountCode
from shopit.models.customer import Customer
from shopit.models.modifier import DiscountCode
from shopit.settings import ERROR_MESSAGES as EM
from shopit.settings import ADDRESS_COUNTRIES


class CartDiscountCodeForm(forms.ModelForm):
    """
    Form that handles entering a cart modifier code.
    """
    class Meta:
        model = CartDiscountCode
        fields = ['code']

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart')
        kwargs['instance'] = CartDiscountCode(cart=self.cart)
        super(CartDiscountCodeForm, self).__init__(*args, **kwargs)
        self.fields['code'].required = False
        self.fields['code'].label = _('Discount code')

    def clean_code(self):
        code = self.cleaned_data.get('code', None)
        if code:
            cart_codes = self.cart.get_discount_codes().values_list('code', flat=True)
            if code in cart_codes:
                raise forms.ValidationError(EM['cart_discount_code_exists'])
            try:
                dc = DiscountCode.objects.valid().get(code=code)
            except DiscountCode.DoesNotExist:
                raise forms.ValidationError(EM['cart_discount_code_invalid'])
            if dc.customer and code not in self.cart.customer.get_discount_codes().values_list('code', flat=True):
                raise forms.ValidationError(EM['cart_discount_code_wrong_customer'])
        return code

    def save(self, commit=True):
        if self.cleaned_data.get('code', None):
            return super(CartDiscountCodeForm, self).save(commit)


class CheckoutFormMixin(object):
    """
    Checkout form mixin ensures request and cart are passed in.
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.cart = kwargs.pop('cart')
        super(CheckoutFormMixin, self).__init__(*args, **kwargs)


class CustomerForm(CheckoutFormMixin, AccountDetailsForm):
    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart')
        return AccountDetailsForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        self.instance.recognize_as_registered()
        return super(CustomerForm, self).save(commit)


class GuestForm(CheckoutFormMixin, CleanEmailMixin, forms.ModelForm):
    email = forms.EmailField(label=_('Email address'))

    class Meta:
        model = get_user_model()
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(GuestForm, self).__init__(*args, **kwargs)
        self.customer = Customer.objects.get_from_request(self.request)
        self.instance = self.customer.user
        self.fields['email'].initial = self.instance.email

    def save(self, commit=True):
        self.customer.recognize_as_guest()
        self.instance.is_active = GUEST_IS_ACTIVE_USER
        if self.instance.is_active:
            password = get_user_model().objects.make_random_password(length=30)
            self.instance.set_password(password)
        self.customer.save()
        return super(GuestForm, self).save(commit)


class AddressForm(CheckoutFormMixin, forms.ModelForm):
    priority = forms.IntegerField(required=False, widget=forms.HiddenInput)
    existant = forms.ModelChoiceField(required=False, queryset=None, label=_('Use existant address'))

    class Meta:
        exclude = ['customer']

    def __init__(self, *args, **kwargs):
        self.field_order = ['existant']  # Place `existant` field at the top.
        super(AddressForm, self).__init__(*args, **kwargs)
        self.customer = Customer.objects.get_from_request(self.request)
        addresses = self.Meta.model.objects.filter(customer=self.customer)
        self.fields['existant'].queryset = addresses
        if not addresses.exists():
            self.fields['existant'].widget = forms.HiddenInput()
        if ADDRESS_COUNTRIES:
            countries = [('', '---------')] + [x for x in ISO_3166_CODES if x in ADDRESS_COUNTRIES]
            self.fields['country'].widget = forms.Select(choices=countries)
        cart_address = getattr(self.cart, '%s_address' % self.Meta.model.__name__.lower().rstrip('address'), None)
        if cart_address:
            self.fields['existant'].initial = cart_address
            for fname in [f.name for f in cart_address._meta.get_fields() if f.name in self.fields]:
                self.fields[fname].initial = getattr(cart_address, fname, '')

    def clean(self):
        existant = self.cleaned_data['existant']
        if existant:
            self.instance = existant  # Set existant as an instance if selected.
            self.cleaned_data['priority'] = existant.priority
            # Populate missing fields in `cleaned_data` with existant data and skip validation.
            for field in [x for x in self.fields if x not in self.cleaned_data]:
                self.cleaned_data[field] = getattr(existant, field)
                del self._errors[field]
        else:
            self.cleaned_data['priority'] = self.Meta.model.objects.get_max_priority(self.customer) + 1
        return super(AddressForm, self).clean()

    def save(self, commit=True):
        instance = super(AddressForm, self).save(commit=False)
        instance.customer = self.customer
        instance.save()
        return instance


class ShippingAddressForm(AddressForm):
    class Meta(AddressForm.Meta):
        model = ShippingAddress


class BillingAddressForm(AddressForm):
    use_shipping_address = forms.BooleanField(label=_('Use shipping address for billing'), required=False)

    class Meta(AddressForm.Meta):
        model = BillingAddress

    def __init__(self, *args, **kwargs):
        super(BillingAddressForm, self).__init__(*args, **kwargs)
        if self.cart.shipping_address and not self.cart.billing_address:
            self.fields['use_shipping_address'].initial = True

    def full_clean(self):
        super(BillingAddressForm, self).full_clean()
        if self.is_bound and self['use_shipping_address'].value():
            self._errors = ErrorDict()

    def is_valid(self):
        return self['use_shipping_address'].value() or super(BillingAddressForm, self).is_valid()

    def save(self, commit=True):
        if not self['use_shipping_address'].value():
            return super(BillingAddressForm, self).save(commit)


class PaymentMethodForm(CheckoutFormMixin, forms.Form):
    payment_modifier = forms.ChoiceField(label=_('Payment method'), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(PaymentMethodForm, self).__init__(*args, **kwargs)
        choices = [x.get_choice() for x in cart_modifiers_pool.get_payment_modifiers() if not x.is_disabled(self.cart)]
        self.fields['payment_modifier'].choices = choices
        if len(choices) == 1:
            self.fields['payment_modifier'].initial = choices[0][0]


class DeliveryMethodForm(CheckoutFormMixin, forms.Form):
    shipping_modifier = forms.ChoiceField(label=_('Delivery method'), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(DeliveryMethodForm, self).__init__(*args, **kwargs)
        choices = [x.get_choice() for x in cart_modifiers_pool.get_shipping_modifiers()
                   if not x.is_disabled(self.cart)]
        self.fields['shipping_modifier'].choices = choices
        if len(choices) == 1:
            self.fields['shipping_modifier'].initial = choices[0][0]


class ExtraAnnotationForm(CheckoutFormMixin, forms.Form):
    annotation = forms.CharField(label=_('Extra annotation for this order'), required=False, widget=forms.Textarea)


class AcceptConditionForm(CheckoutFormMixin, forms.Form):
    accept = forms.BooleanField(label=_('Accept'), required=True, widget=forms.CheckboxInput)
