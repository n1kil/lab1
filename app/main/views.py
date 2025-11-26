from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .forms import UserForm
from .models import *
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import Article, Comment
from .forms import ArticleForm, CommentForm, CustomUserCreationForm
from datetime import date

def index(request):
    # Обновляем главную страницу для отображения статей из БД
    articles = Article.objects.filter(is_published=True).order_by('-created_date')[:5]
    context = {
        'articles': articles,
        'today': date.today()
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def articles(request):
    # Обновляем для работы с реальными статьями из БД
    articles_list = Article.objects.filter(is_published=True).order_by('-created_date')
    context = {
        'articles': articles_list,
        'today': date.today()
    }
    return render(request, "articles.html", context)

def news(request, id):
    # Обновляем для отображения реальной статьи с комментариями
    article = get_object_or_404(Article, id=id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('news', id=id)
    else:
        form = CommentForm()
    
    comments = article.comments.all().order_by('-date')
    
    context = {
        'article': article,
        'form': form,
        'comments': comments
    }
    return render(request, 'article_detail.html', context)

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            messages.success(request, 'Статья успешно создана!')
            return redirect('articles')  # Изменяем на 'articles'
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id, user=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно обновлена!')
            return redirect('articles')  # Изменяем на 'articles'
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form, 'article': article})

@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id, user=request.user)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья успешно удалена!')
        return redirect('articles')  # Изменяем на 'articles'
    return render(request, 'delete_article.html', {'article': article})

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

# ДОБАВЛЯЕМ НОВЫЕ ПРЕДСТАВЛЕНИЯ:

def articles_by_category(request, category):
    """Фильтрация статей по категориям"""
    valid_categories = ['tech', 'science', 'sports', 'politics', 'entertainment']
    if category not in valid_categories:
        messages.error(request, 'Неверная категория')
        return redirect('articles')
    
    articles_list = Article.objects.filter(category=category, is_published=True).order_by('-created_date')
    category_name = dict(Article.CATEGORY_CHOICES)[category]
    
    context = {
        'articles': articles_list,
        'category': category_name,
        'today': date.today()
    }
    return render(request, 'articles_by_category.html', context)

def register(request):
    """Регистрация пользователей"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def articles_list(request):
    """Список всех статей (альтернативное представление)"""
    articles_list = Article.objects.filter(is_published=True).order_by('-created_date')
    context = {
        'articles': articles_list,
        'today': date.today()
    }
    return render(request, 'articles_list.html', context)