from django import forms
from .models import * 
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.Form):
    name = forms.CharField()
    mail = forms.EmailField()
    message = forms.CharField()

