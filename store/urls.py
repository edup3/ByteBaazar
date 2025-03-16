from django.urls import path, include
from .views import HomePageView, StorePageView, RegisterCustomerView, ProductPageView, LoginCustomerView, LogoutCustomerView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('store/', StorePageView.as_view(), name='store'),
    path('register/', RegisterCustomerView.as_view(), name='register'),
    path('login/', LoginCustomerView.as_view(), name='login'),
    path('logout/', LogoutCustomerView.as_view(), name='logout'),
    path('product/<pk>', ProductPageView.as_view(), name='product'),
]
