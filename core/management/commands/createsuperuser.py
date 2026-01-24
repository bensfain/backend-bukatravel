from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import AdminRole

class Command(BaseCommand):
    help = 'Create a superuser with admin role'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Tampilkan pilihan role
        roles = AdminRole.objects.all()
        self.stdout.write("Available roles:")
        for i, role in enumerate(roles, 1):
            self.stdout.write(f"{i}. {role.admin_role_name}")
        
        while True:
            try:
                selected = int(input("Select role number: "))
                admin_role = roles[selected-1]
                break
            except (ValueError, IndexError):
                self.stdout.write("Invalid selection, try again.")
        
        # Input data user
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            admin_role=admin_role
        )
        self.stdout.write("Superuser created successfully!")