from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    VersionCreateView, VersionUpdateView, VersionDeleteView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('version/new/', VersionCreateView.as_view(), name='version_create'),
    path('version/<int:pk>/edit/', VersionUpdateView.as_view(), name='version_update'),
    path('version/<int:pk>/delete/', VersionDeleteView.as_view(), name='version_delete'),
]
