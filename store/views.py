from django.shortcuts import render
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.db.models import Avg
from .forms import RegisterForm, ReviewForm
from .models import Product, Customer, Review, Category, Order, OrderItem
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.urls import reverse
from django.db import models
from django.http import JsonResponse
import requests
from django.views import View
from django.shortcuts import get_list_or_404
from .services.pdf_report import PDFReportGenerator
from .services.excel_report import ExcelReportGenerator
from django.http import HttpResponse
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = 'pub_8735455c9bd5909dd7fa801dd2331956af047'
        url = f'https://newsdata.io/api/1/news?apikey={api_key}&category=technology&language=en'

        try:
            response = requests.get(url)
            data = response.json()
            context['news'] = data.get('results', [])
        except Exception as e:
            print(f"Error al consumir la API de noticias: {e}")
            context['news'] = []

        return context

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
        form.instance.customer = self.request.user
        form.instance.product = Product.objects.get(
            pk=self.kwargs['product_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product', kwargs={'pk': self.kwargs['product_pk']})
    
class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.filter(customer=self.request.user, status='pending').first()
        context['order'] = order
        return context
    
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Obtener o crear la orden pendiente
    order, created = Order.objects.get_or_create(
        customer=request.user,
        status='pending',
        defaults={'total_price': 0}
    )

    # Obtener o crear el OrderItem correspondiente
    order_item, item_created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 1}
    )

    if not item_created:
        order_item.quantity += 1
        order_item.save()

    # Actualizar el total de la orden
    total = order.items.aggregate(total=Sum(models.F('quantity') * models.F('product__price')))['total'] or 0
    order.total_price = total
    order.save()

    # Redirigir a la misma página del producto
    return redirect('product', pk=product.id)

def products_in_stock(request):
    products = Product.objects.filter(stock__gt=0)

    data = []
    for product in products:
        product_url = request.build_absolute_uri(
            reverse('product', args=[product.pk])
        )
        data.append({
            'id': product.pk,
            'name': product.name,
            'price': float(product.price),
            'stock': product.stock,
            'category': product.category.name if product.category else None,
            'url': product_url,
        })

    return JsonResponse(data, safe=False)

class ProductReportView(View):
    def get(self, request, format):
        products = Product.objects.all()
        if format == "pdf":
            generator = PDFReportGenerator()
            response = generator.generate(products)
            response['Content-Disposition'] = 'attachment; filename="products_report.pdf"'
            return response
        elif format == "excel":
            generator = ExcelReportGenerator()
            response = generator.generate(products)
            response['Content-Disposition'] = 'attachment; filename="products_report.xlsx"'
            return response
        else:
            return HttpResponse("Formato no soportado", status=400)