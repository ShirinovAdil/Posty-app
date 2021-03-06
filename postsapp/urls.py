from django.urls import include, path, re_path
from rest_framework import routers
from postsapp import views

router = routers.DefaultRouter()
#router.register(r'commentsViewSet', views.CommentsViewSet)
#router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('comments/', views.CommentApiView.as_view()),
    path('comments/', views.CommentGenericApiView.as_view()),

    path('comments/<int:pk>', views.CommentDetailApiView.as_view()),

    path('posts/', views.PostsListView.as_view()),
    path('posts/<int:pk>', views.PostDetailView.as_view()),
    path('posts/<int:pk>/upvote/', views.upvote_view),


    path('profile/', views.UserApiView.as_view()),



]