from django.test import TestCase
from django.urls import reverse
from store.models import Product, Category

class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)


class ProductModelTest(TestCase):
    def test_create_product(self):
        category = Category.objects.create(name="Hardware")
        product = Product.objects.create(name="Mouse Gamer",price=50,stock=10,category=category) 
        self.assertEqual(product.name, "Mouse Gamer")
        self.assertEqual(product.price, 50)
        self.assertEqual(product.category.name, "Hardware")