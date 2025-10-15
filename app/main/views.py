from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")

def about(request):
    return HttpResponse("Об авторах")

def contact(request):
    return HttpResponse("Свяжитесь с нами по номеру 999")
