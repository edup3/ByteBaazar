from django.shortcuts import render
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from .forms import RegisterForm
from .models import Product, Customer
from .mixins import UserContextMixin

# Create your views here.


class RegisterCustomerView(CreateView):
    template_name = 'store/register.html'
    model = Customer
    form_class = RegisterForm
    success_url = reverse_lazy('home')


class LoginCustomerView(LoginView):
    template_name = 'store/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class LogoutCustomerView(LogoutView):
    success_url = reverse_lazy('home')


class HomePageView(UserContextMixin, TemplateView):
    template_name = 'store/index.html'


class StorePageView(LoginRequiredMixin, UserContextMixin, ListView):
    login_url = '/login/'
    template_name = 'store/items.html'
    model = Product
    context_object_name = 'products'


class ProductPageView(UserContextMixin, DetailView):
    model = Product
    template_name = 'store/product.html'
