from django import forms
 
class UserForm(forms.Form):
    name = forms.CharField()
    mail = forms.CharField()
    message = forms.CharField()