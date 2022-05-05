from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm,AuthenticationForm,
UserChangeForm,PasswordResetForm,SetPasswordForm,PasswordChangeForm)
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomerModel



# User Signup
class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            # 'first_name':forms.TextInput(attrs={'class':'form-control'}),
            # 'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     ok = self.cleaned_data['email']
    #     if ok == '':
    #         raise forms.ValidationError('Required')
    #     else:
    #         ok


class SigninForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','password']

class UserProfileChangeForm(UserChangeForm):
    password =None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {

        'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),

        'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),

        'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),

        'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter E-Mail'}),

    }


class PassChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Old Password'}))
    new_password1 =forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 =forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Re-New Password'}))




city = (('Ahemdabad','Ahemdabad'),)
state = (('Gujarat','Gujarat'),)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        fields = ['name','mobile','email','locality','city','zipcode','state']

        widgets = {
            # 'user':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Mobile Number'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter E-Mail'}),
            'locality':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address'}),
            'city':forms.Select(choices=city,attrs={'class':'form-control'}),
            'zipcode':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Zip-Code'}),
            'state':forms.Select(choices=state,attrs={'class':'form-control'}),
        }

# Password Reset TextBox With Registred E-Mail
class PassResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Registered E-Mail'}))
    
# New Password Set Registred E-Mail Link
class SetNewPassForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm New Password'}))

