from rest_framework import serializers
from posts.models import Post
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'description']


"""Serializer instead of ModelSerializer - no need for the Meta class, only one attribute is needed (prof. picture),
not an entire representation of the Django db Model"""


class ProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    liked_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'liked_users']
        read_only_fields = ['id', 'author', 'created_at', 'liked_users']


class SubmitPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']
