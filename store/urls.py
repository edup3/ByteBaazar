from django.urls import path, include
from . import views
from .views import HomePageView, StorePageView, RegisterCustomerView, ProductPageView, LoginCustomerView, LogoutCustomerView, CreateReviewView, CartView, ProductReportView
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
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('set-language/', set_language, name='set_language'),
    path('api/products-in-stock/', views.products_in_stock, name='products_in_stock'),
    path('report/<str:format>/', ProductReportView.as_view(), name='product_report'),
]
