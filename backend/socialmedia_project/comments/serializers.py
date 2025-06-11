from rest_framework import serializers
from django.db.models.aggregates import Count

from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    comment_likes_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Comment
        fields = ['author', 'post', 'content', 'image', 'parent', 'created_at', 'updated_at', 'comment_likes_count', 'children']
        read_only_fields = ['author', 'post', 'created_at', 'updated_at']
        
    
    def get_children(self, obj):
        children_qs = obj.children.all().annotate(comment_likes_count=Count('likes'))
        if not children_qs.exists():
            return []
        return CommentSerializer(children_qs, many=True, context=self.context).data
    
    # def get_comment_likes(self, obj):
    #     return obj.likes.count()
