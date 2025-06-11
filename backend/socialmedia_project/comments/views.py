from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models.aggregates import Count

from .models import Comment
from posts.models import Post
from .serializers import CommentSerializer
from .permissions import CommentOwnerOrReadOnly


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentOwnerOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        cache_key = f"Comments_for_{self.kwargs.get('post_id')}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 10*60)
        return Response(response.data)
    
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.select_related('author').filter(post_id=post_id, parent__isnull=True).annotate(comment_likes_count=Count('likes'))
    
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        cache.delete(f"Comments_for_{self.kwargs.get('post_id')}")
        serializer.save(author=self.request.user, post=post)
        
    
    def perform_update(self, serializer):
        cache.delete(f"Comments_for_{self.kwargs.get('post_id')}")
        return super().perform_update(serializer)
    
    
    def perform_destroy(self, instance):
        cache.delete(f"Comments_for_{self.kwargs.get('post_id')}")
        return super().perform_destroy(instance)
    
    @action(methods=['post'], detail=False)
    def clear_cache(self, request, **kwargs):
        cache.delete(f"Comments_for_{self.kwargs.get('post_id')}")
        return Response({'detail': 'cache cleared'})