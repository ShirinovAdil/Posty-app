from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model to add extra fields
    """
    birthdate = models.DateField(null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True)


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True)
    content = models.TextField(blank=False, null=True)
    rating = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.author} commented: {self.content[:50]}..."

