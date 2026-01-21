from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Article
from .serializers import ArticleSerializer

@api_view(['GET'])
def articles_api(request):
    articles_list = Article.objects.select_related('user').all().order_by('-created_date')
    
    serializer = ArticleSerializer(
        articles_list, 
        many=True,
        context = {
            'articles': articles_list,
            'title': 'Все статьи',
            'today': timezone.now().date(),
            'category_choices': Article.CATEGORY_CHOICES,
        }
    )
    return Response(serializer.data)


@api_view(['GET'])
def article_detail_api(request, id):
    
    article = get_object_or_404(Article, id=id)
    
    serializer = ArticleSerializer(article)
    
    return Response(serializer.data)
    