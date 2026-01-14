from django import forms
from .models import * 
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.Form):
    name = forms.CharField()
    mail = forms.EmailField()
    message = forms.CharField()

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text'] 
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок'
            }),
            'text': forms.Textarea(attrs={
                'rows': 10,
                'class': 'form-control',
                'placeholder': 'Введите текст статьи'
            })
        }
        labels = {
            'title': 'Заголовок статьи',
            'text': 'Текст статьи'
        }