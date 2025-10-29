from django.db import models

class User(models.Model):
    id = models.IntegerField()
    name = models.CharField()
    mail = models.EmailField()
    hashed_password = models.CharField()
    date = models.DateTimeField()

class Article(models.Model):
    id = models.IntegerField()
    title = models.TextField()
    text = models.TextField()
    created_date = models.DateTimeField()
    user_id = models.IntegerField()