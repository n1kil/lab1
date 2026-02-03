from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

# Статьи

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
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


@api_view(['GET'])
@permission_classes([AllowAny])
def articles_by_category_api(request, category):
    valid_categories = dict(Article.CATEGORY_CHOICES).keys()

    if category not in valid_categories:
        return Response(
            {
                'status': 'error',
                'message': 'Неверная категория',
                'valid_categories': list(valid_categories)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    articles = (
        Article.objects
        .filter(category=category)
        .select_related('user')
        .order_by('-created_date')
    )

    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def article_sorted_by_date_api(request):
    articles = (
        Article.objects
        .order_by('-created_date')
        .select_related('user')
    )
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Комменты

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comments_api(request):

    if request.method == 'GET':
        article_id = request.query_params.get('article', None)

        if article_id:
            # Если передан параметр `article`, фильтруем комментарии по статье
            comments = Comment.objects.filter(article__id=article_id).order_by('-date')
        else:
            # Если не передан параметр, возвращаем все комментарии
            comments = Comment.objects.all().order_by('-date')

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': 'success',
                    'message': 'Комментарий создан',
                    'comment': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'status': 'error',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_detail_api(request, id):
    comment = get_object_or_404(Comment, id=id)


    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


    elif request.method == 'PUT':
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=False
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': 'success',
                    'message': 'Комментарий обновлён',
                    'comment': serializer.data
                }
            )

        return Response(
            {
                'status': 'error',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(
            {
                'status': 'success',
                'message': 'Комментарий удалён'
            },
            status=status.HTTP_204_NO_CONTENT
        )