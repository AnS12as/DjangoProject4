from django.core.mail import send_mail
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from config import settings
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogpost_list.html'
    context_object_name = 'posts'
    queryset = BlogPost.objects.filter(published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self):
        post = super().get_object()
        post.views += 1
        post.save()
        return post


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost_form.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:blogpost_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogpost_confirm_delete.html'
    success_url = reverse_lazy('catalog:blogpost_list')

    def get_object(self):
        post = super().get_object()
        post.views += 1
        post.save()
        if post.views == 100:
            self.send_congratulations_email(post)
        return post

    def send_congratulations_email(self, post):
        subject = 'Поздравляем с достижением 100 просмотров!'
        message = f'Ваша статья "{post.title}" достигла 100 просмотров!'
        recipient_list = ['anastasiya0625@gmail.com']
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

