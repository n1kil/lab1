from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='user.username',
        read_only=True
    )
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'text',
            'category',
            'created_date',
            'author_name',
        )
        read_only_fields = ('id', 'created_date', 'author_name')

    def get_created_date(self, obj):
        return obj.created_date
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Заголовок должен содержать минимум 3 символа"
            )
        
        if len(value) > 200:
            raise serializers.ValidationError(
                "Заголовок не должен превышать 200 символов"
            )
        
        return value
    
    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Текст статьи должен содержать минимум 10 символов"
            )
        
        if len(value) > 10000:
            raise serializers.ValidationError(
                "Текст статьи не должен превышать 10000 символов"
            )
        
        return value
    
    def validate_category(self, value):
        valid_categories = dict(Article.CATEGORY_CHOICES).keys()
        
        if value not in valid_categories:
            raise serializers.ValidationError(
                f"Неверная категория. Допустимые значения: {', '.join(valid_categories)}"
            )
        
        return value
    
    
    
    def validate(self, data):
        return data
   