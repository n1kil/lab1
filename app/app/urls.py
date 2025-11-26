from main import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('feedback/', views.feedback, name="feedback"),
    path('articles/', views.articles, name="articles"),
    path('news/<int:number>/', views.news, name="news"),
    
    # CRUD для статей
    path('create-article/', views.create_article, name="create_article"),
    path('edit-article/<int:id>/', views.edit_article, name="edit_article"),
    path('delete-article/<int:id>/', views.delete_article, name="delete_article"),
    
    # Фильтрация по категориям
    path('articles/<str:category>/', views.articles_by_category, name="articles_by_category"),
    
    # Аутентификация
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name="logout"),
]