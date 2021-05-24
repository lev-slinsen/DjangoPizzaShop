from django import forms
from django.forms import TextInput, DateInput

from .models import Order, LegalOrder


class LegalOrdersForm(forms.Form):
    LegalOrders = forms.ModelChoiceField(
        queryset=LegalOrder.objects.all(),
        empty_label=None,
    )


class LegalOrderForm(forms.ModelForm):
    unp = forms.CharField(widget=TextInput(attrs={
            'id': 'unp',
            'type': 'name',
            'class': 'form-control',
            'onchange': 'validateUnp()',
            'placeholder': ' УНП'}))
    phone = forms.CharField(widget=TextInput(attrs={
            'id': 'phone',
            'type': 'phone',
            'class': 'form-control',
            'onsubmit': 'return validationAll()',
            'onchange': 'validatePhone()',
            'placeholder': '(xx)xxx-xx-xx'}))
    name_firm = forms.CharField(widget=TextInput(attrs={
            'id': 'name_firm',
            'type': 'name',
            'class': 'form-control',
            'oninput': 'validateNameFirm()',
            'onsubmit': 'return validationAll()',
            'placeholder': 'Контактное лицо'}))
    first_name = forms.CharField(widget=TextInput(attrs={
            'id': 'first_name',
            'type': 'name',
            'class': 'form-control',
            'oninput': 'validateName()',
            'onsubmit': 'return validationAll()',
            'placeholder': 'Контактное лицо'}))
    delivery_date = forms.DateField(widget=DateInput(attrs={
            'id': 'delivery_date',
            'type': 'text',
            'onchange': 'validateDate()',
            'autocomplete': 'off',
            'required pattern': '[0-9_-]*',
            'class': 'form-control datetimepicker-input',
            'data-toggle': 'datetimepicker',
            'data-target': '#delivery_date',
            'placeholder': 'Выберите дату'}))
    legal_address = forms.CharField(widget=TextInput(attrs={
            'id': 'legal_address',
            'type': 'text',
            'class': 'form-control',
            'oninput': 'validateAddress()',
            'placeholder': 'Адрес'}))
    delivery_address = forms.CharField(widget=TextInput(attrs={
            'id': 'delivery_address',
            'type': 'text',
            'class': 'form-control',
            'oninput': 'validateDeliveryAddress()',
            'placeholder': 'Адрес'}))
    email = forms.CharField(widget=TextInput(attrs={
            'id': 'email',
            'type': 'text',
            'class': 'form-control',
            'oninput': 'validateEmail()',
            'placeholder': 'Адрес'}))
    comment = forms.CharField(widget=TextInput(attrs={
            'id': 'comment',
            'class': 'form-control',
            'type': 'textarea',
            'size': '40',
            'rows': '5'}), required=False)

    class Meta:
        model = LegalOrder
        fields = ['unp', 'phone', 'name_firm', 'first_name',
                  'delivery_date', 'legal_address', 'delivery_address',
                  'email', 'comment', 'delivery_time', 'payment', ]

    def __init__(self, *args, **kwargs):
        super(LegalOrderForm, self).__init__(*args, **kwargs)
        self.fields['delivery_time'].widget.attrs.update({
                'id': 'delivery_time',
                'onchange': 'validateTime()',
                'class': 'form-control',
                'placeholder': 'Выберите время'})
        self.fields['payment'].widget.attrs.update({
                'id': 'payment',
                'onchange': 'validatePaymentWay()',
                'class': 'form-control',
                'placeholder': 'Выберите способ оплаты'})


class OrderForm(forms.ModelForm):
    phone = forms.CharField(widget=TextInput(attrs={
            'id': 'phone',
            'type': 'phone',
            'class': 'form-control',
            'onsubmit': 'return validationAll()',
            'onchange': 'validatePhone()',
            'placeholder': '(xx)xxx-xx-xx'}))
    first_name = forms.CharField(widget=TextInput(attrs={
            'id': 'first_name',
            'type': 'name',
            'class': 'form-control',
            'oninput': 'validateName()',
            'onsubmit': 'return validationAll()',
            'placeholder': 'Имя'}))
    delivery_date = forms.DateField(widget=DateInput(attrs={
            'id': 'delivery_date',
            'type': 'text',
            'onchange': 'validateDate()',
            'autocomplete': 'off',
            'required pattern': '[0-9_-]*',
            'class': 'form-control datetimepicker-input',
            'data-toggle': 'datetimepicker',
            'data-target': '#delivery_date',
            'placeholder': 'Выберите дату'}))
    address = forms.CharField(widget=TextInput(attrs={
            'id': 'address',
            'type': 'text',
            'class': 'form-control',
            'oninput': 'validateAddress()',
            'placeholder': 'Адрес'}))
    comment = forms.CharField(widget=TextInput(attrs={
            'id': 'comment',
            'class': 'form-control',
            'type': 'textarea',
            'size': '40',
            'rows': '5'}), required=False)

    class Meta:
        model = Order
        fields = ['phone', 'first_name', 'delivery_date', 'delivery_time', 'address', 'payment', 'comment']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['delivery_time'].widget.attrs.update({
                'id': 'delivery_time',
                'onchange': 'validateTime()',
                'class': 'form-control',
                'placeholder': 'Выберите время'})
        self.fields['payment'].widget.attrs.update({
                'id': 'payment',
                'onchange': 'validatePaymentWay()',
                'class': 'form-control',
                'placeholder': 'Выберите способ оплаты'})
