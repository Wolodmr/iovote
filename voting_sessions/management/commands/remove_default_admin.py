from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Remove default admin user'

    def handle(self, *args, **kwargs):
        User.objects.filter(email='admin@example.com').delete()
        self.stdout.write(self.style.SUCCESS('Successfully removed default admin user'))
