from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Article
from .serializers import ArticleSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def articles_api(request):

    if request.method == 'GET':
        articles = Article.objects.select_related('user').order_by('-created_date')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    serializer = ArticleSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                'status': 'error',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(username='aaa')
    except User.DoesNotExist:
        return Response(
            {'error': 'Пользователь aaa не найден'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    article = serializer.save(user=user)

    return Response(
        {
            'status': 'success',
            'message': 'Статья успешно создана',
            'article': ArticleSerializer(article).data
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def article_detail_api(request, id):

    article = get_object_or_404(Article, id=id)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(
            article,
            data=request.data,
            partial=False  
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': 'success',
                    'message': 'Статья обновлена',
                    'article': serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'status': 'error',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
