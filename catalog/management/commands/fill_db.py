import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Fill the database with initial data from fixtures'

    @staticmethod
    def json_read_categories():
        with open('fixtures/categories.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def json_read_products():
        with open('fixtures/products.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_for_create = []
        products_for_create = []

        for category_data in Command.json_read_categories():
            category_fields = category_data['fields']
            category_fields['id'] = category_data['pk']
            categories_for_create.append(Category(**category_fields))

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(categories_for_create)

        for product_data in Command.json_read_products():
            product_fields = product_data['fields']
            product_fields['id'] = product_data['pk']
            product_fields['category'] = Category.objects.get(pk=product_fields['category'])
            products_for_create.append(Product(**product_fields))

        Product.objects.bulk_create(products_for_create)

        self.stdout.write(self.style.SUCCESS('Database filled with initial data from fixtures.'))
