from django.urls import include, path
from rest_framework import routers
from postsapp import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', views.CommentApiView.as_view()),
    path('comments/<int:pk>', views.CommentDetailApiView.as_view()),
    path('posts/', views.PostsListView.as_view()),
    path('posts/<int:pk>', views.PostDetailView.as_view()),
]