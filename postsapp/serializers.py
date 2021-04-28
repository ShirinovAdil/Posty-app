from rest_framework import serializers
from django.contrib.auth.models import User
from postsapp.models import *


class RecursiveCommentSerializer(serializers.Serializer):
    """
    Recursive representation of comments and replies
    """
    def to_representation(self, instance):
        print(f"instance = {instance}")
        serializer = self.parent.parent.__class__(instance, context=self.context)
        print(f"self.parent = {self.parent}")
        print(f"self.parent,parent = {self.parent.parent}")
        print(f"self.parent,parent__class__ = {self.parent.parent.__class__()}")
        return serializer.data


class FilterReplySerializer(serializers.ListSerializer):
    """
    To show only comments with parent=None
    """
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=False)
    replies = RecursiveCommentSerializer(many=True, required=False, allow_null=True)

    class Meta:
        list_serializer_class = FilterReplySerializer
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'replies']


class PostSerializer(serializers.ModelSerializer):
    """
    Representation of a Post
    """
    author = serializers.StringRelatedField(read_only=True)
    rating = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'rating', 'date', 'author', 'comments']


class UserSerializer(serializers.ModelSerializer):
    """
    A representation of a user
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'birthdate', 'avatar']
