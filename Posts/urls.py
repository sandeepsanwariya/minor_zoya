from django.urls import path
from .views import *

app_name = 'post'
urlpatterns = [
    path('profile/dashboard/create-post/', CreatePostView, name='createpost'),
    path('profile/dashboard/my-post/', MyPostView, name='mypost'),
    path('profile/dashboard/delete-post/', DeletePostView, name='deletepost'),
    path('profile/dashboard/all-video-post/', AllVideosView, name='allvideopost'),
    
    path('profile/dashboard/all-image-post/', AllImagesView, name='allimagepost'),
    path('profile/dashboard/image-post/', ImagePostView, name='imagepost'),
    path('profile/dashboard/video-post/', VideoPostView, name='videopost'),
    path('profile/dashboard/save-post/<str:post_category>', SavePostView, name="save-post"),
    path('profile/dashboard/edit-post/<str:post_category>/<str:Id>/', EditPostView, name="edit-post"),
    path('profile/dashboard/update-post/<str:post_category>/<str:Id>/', UpdatePostView, name="update-post"),
    path('profile/dashboard/delete-post/<str:post_category>/<str:Id>/', DeletePostView, name="delete-post"),
    path('profile/dashboard/publish-post/<str:post_category>/<str:Id>/', PublishPostView, name="publish-post"),
    path('profile/dashboard/unpublish-post/<str:post_category>/<str:Id>/', UnPublishPostView, name="unpublish-post"),
    path('profile/dashboard/published-post/<str:post_category>/', PublishedPostView, name="published-post"),
    path('like/', LikeBtnView,name="likebtn"),
 ]