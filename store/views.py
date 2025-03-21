from django.shortcuts import render
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.db.models import Avg
from .forms import RegisterForm, ReviewForm
from .models import Product, Customer, Review, Category

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

    def get_queryset(self):
        # Search bar implementation and category filter implementation
        queryset = super().get_queryset()
        search_query = self.request.GET.get('product')
        filter_query = self.request.GET.get('category')
        if search_query or filter_query:
            return queryset.filter(name__icontains=search_query, category__name__icontains=filter_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_category"] = self.request.GET.get(
            "category", "")
        return context


class ProductPageView(DetailView):
    model = Product
    template_name = 'store/product.html'
# Average Rating Implementation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_object()
        reviews = queryset.reviews
        avg = reviews.aggregate(Avg('rating', default=0))
        context.update({
            'average_rating': avg.get('rating__avg')
        })
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'store/review_form.html'
    form_class = ReviewForm

    def form_valid(self, form):
        print(self.kwargs)
        form.instance.customer = self.request.user
        form.instance.product = Product.objects.get(
            pk=self.kwargs['product_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product', kwargs={'pk': self.kwargs['product_pk']})
