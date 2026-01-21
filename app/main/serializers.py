from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id',
            'title', 
            'text', 
            'created_date', 
            'category',
            'user_id',
            'author_name'  
        ]
        read_only_fields = ('created_date', 'id', 'user_id')