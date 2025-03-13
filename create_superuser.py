import os
from django.contrib.auth import get_user_model
from django.core.management import call_command

def create_superuser():
    User = get_user_model()
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser with username: {username}")
        call_command('createsuperuser', interactive=False, username=username, email=email, password=password)
    else:
        print(f"Superuser {username} already exists.")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intervention_management.settings')
    import django
    django.setup()
    create_superuser()