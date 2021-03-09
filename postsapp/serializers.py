from rest_framework import serializers
from django.contrib.auth.models import User
from postsapp.models import *


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=False)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    rating = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'rating', 'date', 'author', 'comments']


