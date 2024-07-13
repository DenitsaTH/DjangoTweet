from rest_framework import serializers
from posts.models import Post
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'description']


class ProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    liked_users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'liked_users']
        read_only_fields = ['id', 'author', 'created_at', 'liked_users']


class SubmitPostSerialized(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content']
