import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bdms_project.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created successfully: admin / admin123")
else:
    print("Superuser already exists.")
