import factory
from .models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    name = factory.Faker('company')
    price = factory.Faker('random_int', min=200, max=9000)
    description = factory.Faker('text')
    stock = factory.Faker('random_int', min=1, max=100)
