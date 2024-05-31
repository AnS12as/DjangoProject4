from django import forms
from .models import Product, BlogPost


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'manufactured_at']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'published']
