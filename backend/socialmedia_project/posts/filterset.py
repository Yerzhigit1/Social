from django_filters import rest_framework as filters
from .models import Post

class PostFilters(filters.FilterSet):
    author = filters.CharFilter('author__username', lookup_expr='icontains')
    content = filters.CharFilter('content', lookup_expr='icontains')
    post_from = filters.DateFilter('updated_at', lookup_expr='gte')
    post_to = filters.DateFilter('updated_at', lookup_expr='lte')
    
    class Meta:
        model = Post
        fields = ['author', 'content', 'post_from', 'post_to']