from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from paymentgateway.views import *

app_name = 'paymentgateway'
urlpatterns = [
     path('payment/webhook/', Webhook, name='webhook'),



     path('payment/subscribe/<str:creator_username>/', Subscribe, name='subscribe'),
     path('payment/donate/<str:creator_username>/', Donate, name='donation'),
     path('payment/donationvarify/<str:creator_username>/', DonationVerify, name='donationverify'),
     path('payment/cancel-subscription/<str:creator_profileId>/', CancelSubscription, name='cancelsubscription'),
     path('payment/buyproduct/<str:creator_profileId>/<str:customer_profileId>/<str:productId>/', BuyProduct, name='paymentgateway'),
     path('payment/product/thankyou/<str:customer_id>/<str:creator_id>/<str:amount>/<str:productId>', ThankyouForProduct, name='thankyouforproduct'),
     path('payment/redeem/', RedeemAmount, name='redeemamount'),
    
]
