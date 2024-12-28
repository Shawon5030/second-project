from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation


#Registration
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}


#Login
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control' }))

    password = forms.CharField(label=_('Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current_password','class':'form-control' }))

from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'division', 'district', 'thana', 'villorroad', 'zipcode', 'Mobile_number', 'image']


#Password Change
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus': True, 'class':'form-control'}))

    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())


    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}))


#password reset 
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control'}))


#set password form
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    
    new_password2 = forms.CharField(label=_('Confirm new password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))






from .models import *




    
    
from django import forms
from .models import Withdraw


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ['amount', 'method', 'Account_number']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter withdrawal amount',
            }),
            'method': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select payment method',
            }),
            'Account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter account number or payment details',
            }),
        }



