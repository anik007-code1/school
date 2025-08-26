#!/usr/bin/env python3
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import HomepageSlider

# Create a superuser if not exists
try:
    user = User.objects.get(username='admin')
except User.DoesNotExist:
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

# Create sample slider data
sliders = [
    {'order': 1, 'is_active': True},
    {'order': 2, 'is_active': True},
    {'order': 3, 'is_active': True},
]

for slider_data in sliders:
    HomepageSlider.objects.get_or_create(
        order=slider_data['order'],
        is_active=slider_data['is_active'],
        defaults={
            'created_by': user
        }
    )

print('Sample slider data created successfully!')
print('You can now add actual images through the admin panel at:')
print('http://localhost:8001/custom-admin/sliders/')
print('Admin credentials: admin / admin123')