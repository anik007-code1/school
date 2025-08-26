#!/usr/bin/env python3
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import StudentClass, ClasswiseStudentCount

# Create a superuser if not exists
try:
    user = User.objects.get(username='admin')
except User.DoesNotExist:
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

# Create student classes
classes_data = [
    {"name": "Class 1", "code": "1", "order": 1},
    {"name": "Class 2", "code": "2", "order": 2},
    {"name": "Class 3", "code": "3", "order": 3},
    {"name": "Class 4", "code": "4", "order": 4},
    {"name": "Class 5", "code": "5", "order": 5},
]

created_classes = []
for class_data in classes_data:
    cls, created = StudentClass.objects.get_or_create(
        code=class_data["code"],
        defaults={"name": class_data["name"], "order": class_data["order"]}
    )
    created_classes.append(cls)

# Create student counts for 2025
for i, cls in enumerate(created_classes, 1):
    total = 40 + i * 5  # Varying numbers
    male = total // 2 + (i % 3)  # Slight variation
    female = total - male
    
    ClasswiseStudentCount.objects.get_or_create(
        student_class=cls,
        academic_year=2025,
        defaults={
            'total_students': total,
            'total_male': male,
            'total_female': female,
            'updated_by': user
        }
    )

print("Test data created successfully!")
print(f"Created {len(created_classes)} classes with student counts")

# Verify the data
counts = ClasswiseStudentCount.objects.filter(academic_year=2025)
for count in counts:
    print(f"{count.student_class.name}: {count.total_students} students ({count.total_male}M, {count.total_female}F)")
    
