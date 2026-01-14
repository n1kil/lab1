from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    hashed_password = models.TextField()
    created_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    created_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='articles'
    )
    
    def __str__(self):
        return self.title
    