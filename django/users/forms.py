from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'required': True})
