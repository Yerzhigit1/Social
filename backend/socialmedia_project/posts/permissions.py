from rest_framework.permissions import BasePermission, SAFE_METHODS
from datetime import timedelta
from django.utils import timezone


class PostAuthorOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        is_author = obj.author == request.user
        is_admin = request.user.is_staff
        time_since_created = timezone.now() - obj.created_at
        time_blocked = timedelta(minutes=10)
        
        if request.method == 'DELETE':
            if time_since_created < time_blocked and not is_admin:
                return False
            
        return is_admin or is_author
            
    