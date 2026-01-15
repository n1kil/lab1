from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from .forms import *
from .models import *
import random

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def articles(request):
    articles_list = Article.objects.select_related('user').all().order_by('-created_date')
    
    context = {
        'articles': articles_list,
        'title': 'Все статьи',
        'today': timezone.now().date(),
        'category_choices': Article.CATEGORY_CHOICES,
    }
    return render(request, "articles.html", context)

def news(request, number):
    return HttpResponse(f"Статья {number}")

def feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mail = request.POST.get("mail")
        message = request.POST.get("message")
        context = {
            "form": UserForm(),  
            "submitted_data": {
                "name": name,
                "mail": mail,
                "message": message
            }
        }
        
        return render(request, "feedback.html", context)
    else:
        userform = UserForm()
        return render(request, "feedback.html", {"form": userform})
    

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user  
            article.save()
            return redirect('articles')
    else:
        form = ArticleForm()
    
    return render(request, 'create_article.html', {
        'form': form,
        'title': 'Создать статью'
    })

@login_required  
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'create_article.html', {
        'form': form,
        'title': 'Редактировать статью',
        'article': article
    })

@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    
    if request.method == 'POST':
        article.delete()
        return redirect('articles')
    
    return render(request, 'delete_article.html', {
        'article': article
    })



def articles_by_category(request, category):
    valid_categories = dict(Article.CATEGORY_CHOICES).keys()
    
    if category not in valid_categories:
        return render(request, 'category_error.html', {
            'category': category,
            'valid_categories': dict(Article.CATEGORY_CHOICES),
            'category_choices': Article.CATEGORY_CHOICES,
        })
    
    articles_list = Article.objects.filter(
        category=category
    ).select_related('user').order_by('-created_date')
    
    category_name = dict(Article.CATEGORY_CHOICES).get(category, category)
    
    context = {
        'articles': articles_list,
        'title': f"Статьи: {category_name}",
        'category': category,
        'category_name': category_name,
        'today': timezone.now().date(),
        'category_choices': Article.CATEGORY_CHOICES,
    }
    return render(request, "articles.html", context)



def article_detail(request, id):
    """Страница статьи с комментариями"""
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()  
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article  
            comment.save()
            return redirect('article_detail', id=article.id)
    else:
        form = CommentForm()
    
    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'today': timezone.now().date()
    }
    return render(request, 'article_detail.html', context)



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Пароли не совпадают'})
        
        try:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('articles')
        except:
            return render(request, 'register.html', {'error': 'Пользователь уже существует'})
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('articles')
        else:
            return render(request, 'login.html', {'error': 'Неверные данные'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('articles')