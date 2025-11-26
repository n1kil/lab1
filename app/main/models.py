from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Технологии'),
        ('science', 'Наука'),
        ('sports', 'Спорт'),
        ('politics', 'Политика'),
        ('entertainment', 'Развлечения'),
    ]
    
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tech')
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def was_published_today(self):
        return self.created_date.date() == timezone.now().date()

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Комментарий от {self.author_name}"