from typing import Any
from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control',
    }))
    confirm_password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Repeat Password',
        'class':'form-control',
    }))

    
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

    def __init__(self,*args,**kwargs):

        super(RegisterForm,self).__init__(*args,**kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control' #it will loop all the fields and add the class 'form-control'

    def clean(self):
        clean_data = super(RegisterForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match'
            )