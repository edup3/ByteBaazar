from django.urls import path
from .views import HomePageView, StorePageView, RegisterCustomerView, ProductPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('store/', StorePageView.as_view(), name='store'),
    path('register/', RegisterCustomerView.as_view(), name='register'),
    path('product/<pk>', ProductPageView.as_view(), name='product')
]
