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
    

# views.py
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            # ВАЖНО: form.save() НЕ БУДЕТ РАБОТАТЬ, потому что нет поля user в форме!
            # Вместо этого создаем статью вручную
            
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            category = form.cleaned_data['category']  # получаем категорию
            
            users = User.objects.all()
            
            if users.exists():
                random_user = random.choice(list(users))
                
                article = Article.objects.create(
                    title=title,
                    text=text,
                    category=category,  # добавляем категорию
                    created_date=timezone.now().date(),
                    user=random_user
                )
                print(f"✅ Создана статья: '{title}' (категория: {category})")
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
                    category=category,  # добавляем категорию
                    created_date=timezone.now().date(),
                    user=test_user
                )
                print(f"✅ Создана статья с тестовым автором: '{title}'")
            
            return redirect('articles')
        else:
            print("❌ Форма невалидна:", form.errors)
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