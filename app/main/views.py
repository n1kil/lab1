from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .forms import UserForm

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def articles(request):
    articles = [
        {'title': 'Основы Python', 'date': timezone.datetime(2024, 1, 15)},
        {'title': 'Сегодняшняя статья', 'date': timezone.now()},
        {'title': 'Базы данных в Django', 'date': timezone.datetime(2024, 1, 5)},
        {'title': 'fdfdf', 'date': timezone.now()},
    ]
    
    context = {
        'articles': articles,
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