from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer, PublicUserSerializer
from comments.serializers import CommentSerializer


class PostSerializers(serializers.ModelSerializer):
    content = serializers.CharField(required=True)
    author = PublicUserSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id','author','content', 'image', 'created_at', 'updated_at', 'like_count', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'like_count']


    def get_comments(self, obj):
        qs = obj.comments.filter(parent__isnull=True)
        if not qs.exists():
            return []
        return CommentSerializer(qs, many=True, context=self.context).data
    
    
    def validate_content(self, value):
        if len(value) == 0 or value == '':
            raise serializers.ValidationError('Content can not be empty')
        return value
    
    
    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image too large. Max 2MB.')
        
        if value.content_type not in ['image/jpeg', 'image/png']:
            raise serializers.ValidationError('Only JPEG and PNG are allowed.')
        
        return value