from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from catalog.views import home
from config import settings

urlpatterns = [
    path('', home, name='home'),
    path('products/', include('catalog.urls', namespace='catalog')),
    path('users/', include('users.urls', namespace='users')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
