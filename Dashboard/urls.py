from django.urls import path
from .views import *

app_name = 'dashboard'
urlpatterns = [
    path('profile/dashboard/', DashboardView, name='dashboard'),
    path('profile/dashboard/your-supporting', YourSupporting, name='yoursupporting'),
    path('profile/dashboard/followers/', FanpageView, name='fanpage'),
    path('profile/dashboard/Search/', SeachpageView, name='searchpage'),
    path('profile/dashboard/memberships/', Memberships, name='memberships'),
    path('profile/dashboard/redeem/', RedeemPage, name='redeempage'),
]
