from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Profile, User
from .serializers import UserSerializer, ProfileSerializer
from .permissions import OwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filterset import ProfileFilter
 
    
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOrReadOnly]
    lookup_field = 'user__username'
    queryset = Profile.objects.select_related('user').all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfileFilter
    
    def create(self, request, *args, **kwargs):
        return Response({'detail': 'Profile creation is handled automatically.'}, status=status.HTTP_403_FORBIDDEN)
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        username = self.kwargs.get(self.lookup_field)
        
        try:
            obj = queryset.get(user__username=username)
            
        except Profile.DoesNotExist:
            raise NotFound(f"Profile with username {username} not found")
    
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_visibility(self, request, user__username=None):
        profile = self.get_object()
        
        if profile.user != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        
        profile.is_public = not profile.is_public
        profile.save()
        return Response({"is_public": profile.is_public})
    
    
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        
        except Profile.DoesNotExist:
            raise NotFound('Profile not found')
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        serializer = self.get_serializer(profile, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)