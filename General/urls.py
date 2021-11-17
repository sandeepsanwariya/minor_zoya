from django.urls import path
from .views import *

app_name = 'general'
urlpatterns = [
    path('', LoginForm, name='login'),
    path('profile/logout/', logout, name='logout'),
    path('profile/signup/', signup, name='signup'),
    path('profile/verify/', Verify, name='verify'),
    path('profile/generate-otp/', GenerateOtp, name='generateotp'),
    path('signup/create-profile/', CreateProfile, name='profile'),
    path('profile/change-password/', ChangePassword, name='passwordreset'),
    path('profile/change-avatar/', ChangeAvatar, name='changeavatar'),
    path('profile/edit-profile/', EditProfile, name='editprofile'),
    path('profile/save-image/<str:location>/<str:prof_id>', SaveImage, name='saveimage'),
    path('testurl/', TestUrl, name='testurl'),
    path('post/<str:username>/<str:type>/<str:post_id>/', PostsDetailPage, name='testurl'),
    
    path('notifications/mark-as-read/<str:notifi_id>/<str:userprofile_id>', MarkAsRead, name='markasread'),
    path('notifications/mark-allas-read/<str:userprofile_id>', MarkAllAsRead, name='markallasread'),
    path('change/email-number/', ChangeEmailNumber, name='change_email_number'),
    path('profile/edit-profile/banksettings/', BankSetting, name='banksetting'),
    path('profile/edit-profile/editbanksettings/', BankEditSetting, name='editbanksetting'),
    path('profile/edit-profile/publicProfileSetting/', PublicProfileSetting, name='publicprofilesetting'),
    path('profile/edit-profile/publicProfileSettingDone/', PublicProfileSettingDone, name='publicprofilesettingdone'),
    path('profile/update-shipping-addr/<str:product_id>/<str:creator_profileId>', UpdateShippingAddr, name='updateshippingaddr'),
]
