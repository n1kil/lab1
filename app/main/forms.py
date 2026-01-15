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
        fields = ['title', 'text', 'category'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите заголовок статьи'
        })
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Введите текст статьи...'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control'
        })

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author_name']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите ваш комментарий...'
            }),
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            })
        }
        labels = {
            'text': 'Текст комментария',
            'author_name': 'Ваше имя'
        }