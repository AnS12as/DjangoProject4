from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from catalog.forms import ProductForm
from catalog.models import Product
from .models import Version
from .forms import VersionForm


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        for product in products:
            current_version = product.versions.filter(is_current=True).first()
            product.current_version = current_version
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        current_version = product.versions.filter(is_current=True).first()
        context['current_version'] = current_version
        print(f"Current version for product {product.name}: {current_version}")
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_edit.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'version/version_form.html'
    success_url = reverse_lazy('catalog:product_list')


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'version/version_form.html'
    success_url = reverse_lazy('catalog:product_list')


class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'version/version_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
