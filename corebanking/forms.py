from django import forms
from django.contrib.auth.models import User
from corebanking.models import BankAccount

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["username","password"]

class BankAccountForm(forms.ModelForm):
    class Meta:
        model=BankAccount
        fields=["name","account_type"]