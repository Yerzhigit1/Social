from rest_framework.serializers import ModelSerializer

from .models import Follower

class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follower
        fields = ['follower', 'following_to', 'created_at']
        read_only_fields = ['follower', 'following_to', 'created_at']