from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create example users: superuser, admin, regular user"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_superuser('superadmin', 'superadmin@example.com', 'superpass123')
            self.stdout.write(self.style.SUCCESS('Created superadmin user'))

        if not User.objects.filter(username='adminuser').exists():
            User.objects.create_user('adminuser', 'admin@example.com', 'adminpass123', is_staff=True)
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        if not User.objects.filter(username='regularuser').exists():
            User.objects.create_user('regularuser', 'user@example.com', 'userpass123')
            self.stdout.write(self.style.SUCCESS('Created regular user'))