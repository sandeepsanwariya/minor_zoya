"""zocaya_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from General.views import ProfileFilterView, UserProfilePages, Follow, Unfollow, PostsDetailPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Posts.urls', namespace='posts')),
    path('', include('General.urls', namespace='generals')),
    path('', include('Dashboard.urls', namespace='dashboards')),
    path('', include('Store.urls', namespace='store')),
    path('', include('paymentgateway.urls', namespace='paymentgateway')),
    path('accounts/', include('allauth.urls')),
    path('<str:username>/', ProfileFilterView, name="profile-filter"),
    path('<str:username>/user-profile/<str:type>/', UserProfilePages, name="userprofilepages"),
    path('follow/<str:username>', Follow, name="followpage"),
    path('unfollow/<str:username>', Unfollow, name="unfollowpage"),
    path('post/<str:username>/<str:type>/<str:post_id>', PostsDetailPage, name="postsdetailpage"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)