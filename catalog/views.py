# /path/to/your/project/catalog/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.cache import cache

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from catalog.services import get_products, get_categories


@cache_page(60 * 15)
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def category_list(request):
    categories = get_categories()
    return render(request, 'category_list.html', {'categories': categories})


class ProductListView(LoginRequiredMixin, ListView):
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


class ProductDetailView(LoginRequiredMixin, DetailView):
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('catalog:product_list')  # Redirect to the product list after a successful update

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm('catalog.change_product')

    def handle_no_permission(self):
        return redirect('no_permission')


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.owner and not request.user.has_perm('catalog.change_product'):
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_detail', pk=product.pk)  # Use namespaced URL here
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/edit_product.html', {'form': form})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'version/version_form.html'
    success_url = reverse_lazy('catalog:product_list')


class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'version/version_form.html'
    success_url = reverse_lazy('catalog:product_list')


class VersionDeleteView(LoginRequiredMixin, DeleteView):
    model = Version
    template_name = 'version/version_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
