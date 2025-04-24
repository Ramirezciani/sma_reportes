from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.conf import settings

class Command(BaseCommand):
    help = 'Ensure default groups exist with correct permissions'

    def handle(self, *args, **options):
        default_groups = getattr(settings, 'DEFAULT_GROUPS', {})
        
        for group_name, group_config in default_groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group already exists: {group_name}'))
            
            # Clear existing permissions
            group.permissions.clear()
            
            # Add new permissions
            for perm_codename in group_config.get('permissions', []):
                try:
                    app_label, codename = perm_codename.split('_', 1)
                    perm = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                    group.permissions.add(perm)
                    self.stdout.write(f'Added permission: {perm_codename} to {group_name}')
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f'Permission not found: {perm_codename}'
                    ))
        
        self.stdout.write(self.style.SUCCESS('Finished ensuring groups'))
