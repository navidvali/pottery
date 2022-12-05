from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class CustomRegister(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields =  UserCreationForm.Meta.fields + ("email",)


class AccountDetailsForm(ModelForm):
    class Meta:
        model = AccountDetails
        fields = ['address',]


class CouponsForm(ModelForm):
    class Meta:
        model = Coupons
        fields = ['coupon_code', 'percent']

