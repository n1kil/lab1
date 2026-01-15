from django.db import models
from django.utils import timezone

# class User(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#     hashed_password = models.TextField()
#     created_date = models.DateField(default=timezone.now)
    
#     def __str__(self):
#         return self.name

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Технологии'),
        ('science', 'Наука'),
        ('sport', 'Спорт'),
        ('art', 'Искусство'),
        ('education', 'Образование'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=30)
    text = models.TextField()
    created_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE,
        related_name='articles'
    )
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='other'
    )
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"



class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Статья'
    )
    author_name = models.CharField(max_length=100, verbose_name='Имя автора')
    
    def __str__(self):
        return f"Комментарий от {self.author_name} к статье '{self.article.title}'"
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'