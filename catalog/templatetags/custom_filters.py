from django import template
from django.conf import settings
from urllib.parse import urljoin

register = template.Library()


@register.filter(name='media_url')
def media_url(path):
    return urljoin(settings.MEDIA_URL, path)
