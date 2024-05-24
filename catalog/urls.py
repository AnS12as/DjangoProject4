from django.conf import settings
from django.templatetags.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import product_list, product_detail, product_edit

app_name = CatalogConfig.name

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', product_edit, name='product_edit'),
]

