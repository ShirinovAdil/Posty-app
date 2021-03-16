from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view

from postsapp.models import Comment
from postsapp.serializers import *
import postsapp.permissions as custom_permissions

from django.http import Http404
from rest_framework.filters import SearchFilter


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return a list of all comments
        """
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new comment to specific POST
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        GET detail view of a comment
        """
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        if comment:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an existing comment object
        """
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an existing comment object
        """
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostsListView(generics.ListAPIView):
    """
    Returns a list of posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Post.objects.all()
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__contains=title)
        return queryset

    def post(self, request):
        """
        Create a new post
        """
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns, Updates or Deletes a certain post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [custom_permissions.IsAuthorOrReadOnly]


@api_view(['POST'])
def upvote_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.rating += 1
        post.save()
        return Response({"Success": True}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"Success": False}, status=status.HTTP_400_BAD_REQUEST)


class UserApiView(APIView):

    def get(self, request):
        user = request.user
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


