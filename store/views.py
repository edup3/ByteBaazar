from django.shortcuts import render
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from .forms import RegisterForm
from .models import Product, Customer


# Create your views here.


class RegisterCustomerView(CreateView):
    template_name = 'store/register.html'
    model = Customer
    form_class = RegisterForm
    success_url = reverse_lazy('home')


class HomePageView(TemplateView):
    template_name = 'store/index.html'


class StorePageView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    template_name = 'store/items.html'
    model = Product
    context_object_name = 'products'


class ProductPageView(DetailView):
    model = Product
    template_name = 'store/product.html'
