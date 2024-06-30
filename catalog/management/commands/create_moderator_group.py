from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product


class Command(BaseCommand):
    help = 'Create moderator group with specific permissions'

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(name='Moderators')

        permissions = Permission.objects.filter(
            content_type__app_label='catalog',
            codename__in=[
                'change_product',
                'delete_product',
                'view_product',
                'can_publish_product',
                'can_unpublish_product'
            ]
        )

        moderator_group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Moderator group created with permissions'))
