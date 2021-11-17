from django.urls import path
from .views import AllProductsView, StoreView

app_name = 'store'
urlpatterns = [
    path('profile/dashboard/store/', StoreView, name='store'),
    path('profile/dashboard/all-product-post/', AllProductsView, name='allproductpost'),
]