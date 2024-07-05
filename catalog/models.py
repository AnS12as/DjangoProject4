# catalog/models.py
from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


def some_expensive_function(product):
    return f"Expensive result for {product.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manufactured_at = models.DateField(verbose_name='Дата производства продукта', null=True, blank=True)
    published = models.BooleanField(default=False, verbose_name='Опубликован')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец',
                              related_name='products')

    def expensive_computation(self):
        cache_key = f'product_{self.id}_expensive_computation'
        result = cache.get(cache_key)

        if not result:
            result = some_expensive_function(self)
            cache.set(cache_key, result, 600)

        return result

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[str(self.id)])

    class Meta:
        permissions = [
            ('can_publish_product', 'Can publish product'),
            ('can_unpublish_product', 'Can unpublish product'),
        ]

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=20)
    version_name = models.CharField(max_length=255)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.version_name} ({self.version_number})"


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    preview = models.ImageField(upload_to='blog_previews/', null=True, blank=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
