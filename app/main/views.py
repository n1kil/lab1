from django.shortcuts import render, redirect, get_object_or_404
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
    articles_from_db = Article.objects.select_related('user').all()
    
    context = {
        'articles': articles_from_db,  
        'today': timezone.now().date()
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
    

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            
            users = User.objects.all()
            
            if users.exists():
                users_list = list(users)
                random_user = random.choice(users_list)
                
                article = Article.objects.create(
                    title=title,
                    text=text,
                    created_date=timezone.now().date(),
                    user=random_user  
                )
            else:
                test_user = User.objects.create(
                    name='Тестовый автор',
                    email='test@example.com',
                    hashed_password='test123',
                    created_date=timezone.now().date()
                )
                article = Article.objects.create(
                    title=title,
                    text=text,
                    created_date=timezone.now().date(),
                    user=test_user  
                )
            
            return redirect('articles')
    
    else:
        form = ArticleForm()
    
    return render(request, 'create_article.html', {
        'form': form,
        'title': 'Создать статью'
    })

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

def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    
    if request.method == 'POST':
        article.delete()
        return redirect('articles')
    
    return render(request, 'delete_article.html', {
        'article': article
    })