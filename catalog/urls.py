from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    VersionCreateView, VersionUpdateView, VersionDeleteView, product_detail, edit_product, home, category_list

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', cache_page(60 * 15)(product_detail), name='product_detail'),
    path('products/<int:pk>/edit/', edit_product, name='edit_product'),
    path('categories/', category_list, name='category_list'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('version/new/', VersionCreateView.as_view(), name='version_create'),
    path('version/<int:pk>/edit/', VersionUpdateView.as_view(), name='version_update'),
    path('version/<int:pk>/delete/', VersionDeleteView.as_view(), name='version_delete'),
]
