from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models.aggregates import Count
from rest_framework.permissions import IsAuthenticated

from .models import Follower
from .serializers import FollowSerializer
from users.models import User

class FollowViewSet(CreateModelMixin, GenericViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
        
    def create(self, request, *args, **kwargs):
        target_id = request.data.get('target_id')
        target_user = get_object_or_404(User, id=target_id)
        if target_user == request.user:
            return Response({'error': 'You cant follow yourself'}, status=400)
        
        followed, create = Follower.objects.get_or_create(following_to=target_user, follower=request.user)
        
        if not create:
            followed.delete()
            return Response({'followed': False})
        return Response({'followed': True})
    
    
    @action(methods=['get'], detail=False)
    def my_followers(self, request, *args, **kwargs):
        me = get_object_or_404(User, id=request.user.id)
        my_followers = me.followers.all()
        serialized = self.get_serializer(my_followers, many=True)
        return Response({'followers': serialized.data})
    
    
    @action(methods=['get'], detail=False)
    def ifollowed_to(self, request, *args, **kwargs):
        me = get_object_or_404(User, id=request.user.id)
        ifollowed = me.following.all()
        serialized = self.get_serializer(ifollowed, many=True)
        return Response({'ifollowed': serialized.data})