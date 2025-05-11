from django.urls import path, include
from .views import HomePageView, StorePageView, RegisterCustomerView, ProductPageView, LoginCustomerView, LogoutCustomerView, CreateReviewView
from django.views.i18n import set_language

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('store/', StorePageView.as_view(), name='store'),
    path('register/', RegisterCustomerView.as_view(), name='register'),
    path('login/', LoginCustomerView.as_view(), name='login'),
    path('logout/', LogoutCustomerView.as_view(), name='logout'),
    path('product/<int:pk>', ProductPageView.as_view(), name='product'),
    path('product/addreview/<int:product_pk>',
         CreateReviewView.as_view(), name='add_review'),
    path('set-language/', set_language, name='set_language'),

]
