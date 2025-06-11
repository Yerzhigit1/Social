from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import Like, CommentLike
from posts.models import Post
from .serializers import LikeSerializer, CommentLikeSerializer
from comments.models import Comment

class LikesViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=self.request.user)
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
    def destroy(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        like = Like.objects.filter(post__id=post_id, user=self.request.user)
        if like:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Like not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    
class CommentLikeViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        comment_id = request.data.get('comment')
        comment = get_object_or_404(Comment, id=comment_id)
        like, created = CommentLike.objects.get_or_create(comment=comment, user=self.request.user)
        if not created:
            like.delete()
            return Response({'liked': False}, status=status.HTTP_204_NO_CONTENT)
        return Response({'liked': True}, status=status.HTTP_201_CREATED)
