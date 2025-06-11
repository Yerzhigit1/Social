from rest_framework import serializers 
from .models import User, Profile
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True, validators=[UniqueValidator(User.objects.all())])
    full_name = serializers.CharField(required=True, min_length=5)
        
        

    def validate_username(self, value):
        import re
        if not re.match(r'^\w+$', value):
            raise serializers.ValidationError('Only alphanumeric characters and underscores are allowed.')
        return value


    def validate_full_name(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Fullname can not be less than 5 symbols')
        return value
    
    
    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError('Passwords dont match')
        return attrs
    
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('re_password', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user        
    
    class Meta:
        model = User
        fields = ['public_id', 'email', 'username', 'full_name','is_superuser', 'is_active', 'is_staff', 'date_joined', 'password', 're_password']
        read_only_fields = ['public_id','is_superuser', 'is_active', 'is_staff', 'date_joined']
        
        
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['public_id', 'username', 'full_name']    


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    
    
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'avatar', 'cover', 'location', 'is_public', 'created_at', 'updated_at', 'username', 'email', 'followers', 'follows' ]
        read_only_fields = ['created_at', 'updated_at']
        
    def get_followers(self, obj):
        return obj.user.followers.count()
    
    def get_follows(self, obj):
        return obj.user.following.count()