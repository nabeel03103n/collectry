from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

from django import forms

class TransactionForm(forms.Form):
    messageType = forms.CharField(max_length=20)
    merchantId = forms.CharField(max_length=20)
    serviceId = forms.CharField(max_length=20)
    orderId = forms.CharField(max_length=20)
    customerId = forms.CharField(max_length=20)
    transactionAmount = forms.DecimalField(max_digits=10, decimal_places=2)
    currencyCode = forms.CharField(max_length=3)
    requestDateTime = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy'}))
    successUrl = forms.URLField()
    failUrl = forms.URLField()
    additionalField1 = forms.CharField(max_length=50, required=False)
    additionalField2 = forms.CharField(max_length=50, required=False)
    additionalField3 = forms.CharField(max_length=50, required=False)
    additionalField4 = forms.CharField(max_length=50, required=False)
    additionalField5 = forms.CharField(max_length=50, required=False)