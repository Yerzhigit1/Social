from django_filters import rest_framework as filters
from .models import Profile

class ProfileFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    
    class Meta:
        model = Profile
        fields = ['username', 'email']