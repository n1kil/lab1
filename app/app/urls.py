from main import views
from django.urls import path
from main import api_views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.index, name="home"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('feedback', views.feedback,  name="feedback"),
    path('articles', views.articles, name="articles"),
    path('news/<int:number>/', views.news, name="news"),
    path('create_article', views.create_article, name="create_article"),
    path('edit-article/<int:id>/', views.edit_article, name='edit_article'),
    path('delete-article/<int:id>/', views.delete_article, name='delete_article'),
    path('articles/<str:category>/', views.articles_by_category, name='articles_by_category'),
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('api/articles/', api_views.articles_api, name='api_articles'),
    path('api/articles/<int:id>/', api_views.article_detail_api, name='api_article_detail'),
    path('api/articles/category/<str:category>/', api_views.articles_by_category_api, name='api_articles_by_category'),
    path('api/articles/sort/date/', api_views.article_sorted_by_date_api, name="article_sorted_by_date_api"),
    path('api/comment/', api_views.comments_api, name='api_comments'),
    path('api/comment/<int:id>/', api_views.comment_detail_api, name="api_comment_detail"),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]