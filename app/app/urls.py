from main import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="home"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('feedback', views.feedback,  name="feedback"),
    path('articles', views.articles, name="articles"),
    path('news/<int:number>/', views.news, name="news"),
    path('create_article', views.create_article, name="create_article")
]
