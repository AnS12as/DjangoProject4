# Django Project

## Задание 1: Начало работы

Для начала работы над задачей выполните следующие шаги:

1. Настройте виртуальное окружение:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # Для Windows используйте myenv\Scripts\activate

## Задание 2
   pip install django
   django-admin startproject myproject
   cd myproject
   python manage.py startapp catalog
   from django.urls import path
   from . import views

   urlpatterns = [
  path('', views.home, name='home'),
 path('contact/', views.contact, name='contact'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
]

## Задание 3
Создайте папку templates в директории catalog.

Внутри папки templates создайте две HTML страницы: home.html и contact.html.

## Задание 4

from django.shortcuts import render

def home(request):
    return render(request, 'catalog/home.html')

  from django.shortcuts import render

def contact(request):
    return render(request, 'catalog/contact.html')

## Запуск проекта

python manage.py migrate
python manage.py runserver



