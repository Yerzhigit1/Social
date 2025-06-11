from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models.aggregates import Count

from .models import Post
from likes.models import Like
from .serializers import PostSerializers
from .permissions import PostAuthorOrReadOnly
from .filterset import PostFilters
from .throttling import PostCreateThrottlle



class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, PostAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilters
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_queryset(self):
        return Post.objects.select_related('author').all().annotate(like_count=Count('posts_likes'))
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
        
    def get_throttles(self):
        if self.action == 'create':
            self.throttle_classes = [PostCreateThrottlle]
        return super().get_throttles()
    
    
    def list(self, request, *args, **kwargs):
        cache_key = 'posts_list'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*5)
        return response
        
    
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f'post_{pk}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*10)
        return response
    
    
    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete(f'post_{instance.pk}')
        cache.delete('posts_list')
        cache.delete('trending_posts')
        
    
    def perform_destroy(self, instance):
        cache.delete(f'post_{instance.pk}')
        cache.delete('posts_list')
        cache.delete('trending_posts')
        instance.delete()
    # def update(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     cache_key = f'post_{pk}'
    #     cache.delete(cache_key)
    #     return super().update(request, *args, **kwargs)
    
    
    @action(detail=False, methods=['get'], permission_classes=[PostAuthorOrReadOnly])
    def my_posts(self, request):
        cache_key = f'post_by_{request.user.id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        try:
            posts = Post.objects.filter(author=request.user)
        except Post.DoesNotExist:
            raise NotFound('Posts not found')
        
        serializer = self.get_serializer(posts, many=True)
        response = Response(serializer.data)
        cache.set(cache_key, response.data, 60*10)
        return response
        
        
    @action(methods=['get'], detail=False)
    def trending(self, request):
        cache_key = 'trending_posts'
        popular_posts = cache.get(cache_key)
        if popular_posts:
            return Response(popular_posts)
        posts = Post.objects.all().annotate(like_count=Count('posts_likes')).order_by('-like_count')[:3]
        serializer = self.get_serializer(posts, many=True)
        cache.set(cache_key, serializer.data, 60*10)
        return Response(serializer.data)
    
    
    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def is_liked(self, request, pk=None):
        post = self.get_object()
        current_user = request.user
        liked = Like.objects.filter(post=post, user=current_user).exists()
        return Response({'liked': liked})
    
    
    @action(methods=['post'], detail=False)
    def clear_cache(self, request):
        cache.delete('trending_posts')
        cache.delete('posts_list')
        return Response({'detail': 'cache cleared'})