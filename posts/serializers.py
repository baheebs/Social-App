from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(write_only=True) 
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'mobile']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        """
        Validates the password using Django's built-in password validation.
        Ensures it meets the minimum strength requirements.
        """
        try:
            validate_password(value)  # Uses Django's validators from settings
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        mobile = validated_data.pop('mobile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.update_or_create(user=user, defaults={'mobile': mobile})
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user details (read-only).
    """
    mobile = serializers.CharField(source="profile.mobile", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'mobile']

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'created_by', 'is_published', 'created_at', 'likes_count']
        read_only_fields = ['created_by', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['user']

class PostListSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    created_by = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'created_by', 'is_published', 'created_at', 'likes_count']
