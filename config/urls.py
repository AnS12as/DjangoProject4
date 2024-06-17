from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('products/', include('catalog.urls', namespace='catalog')),
                  path('users/', include('users.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
