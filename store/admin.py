from django.contrib import admin
from .models import Customer, Product, Review, Category, Order, OrderItem

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
