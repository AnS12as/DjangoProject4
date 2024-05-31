from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_edit.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_edit.html', {'form': form})
