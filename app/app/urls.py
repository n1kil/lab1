from main import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('contact', views.contact),
]
