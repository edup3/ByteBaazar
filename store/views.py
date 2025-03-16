from django.shortcuts import render
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from .forms import RegisterForm
from .models import Product, Customer, Review

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


class HomePageView(TemplateView):
    template_name = 'store/index.html'


class StorePageView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'store/items.html'
    model = Product
    context_object_name = 'products'


class ProductPageView(DetailView):
    model = Product
    template_name = 'store/product.html'


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'store/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.kwargs['pk']})
