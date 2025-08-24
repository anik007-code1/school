from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import (
    Notice, Teacher, CommitteeMember, Headmaster, SchoolInfo,
    GalleryCategory, GalleryImage, NavigationLink, ContactInfo,
    ExamType, StudentClass, Student, ExamResult, HomepageSlider
)
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populates the database with demo data'

    def handle(self, *args, **options):
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Create School Info
        school_info = SchoolInfo.objects.create(
            name="Noagaon High School",
            tagline="Excellence in Education Since 1950",
            address="123 School Road, Noagaon, Bangladesh",
            phone="+880 1234-567890",
            email="info@noagaonhighschool.edu.bd",
            website="https://noagaonhighschool.edu.bd",
            established_year=1950,
            about="""Noagaon High School is a prestigious educational institution with a rich history of academic excellence. 
            Founded in 1950, our school has been nurturing young minds and shaping future leaders for over seven decades.
            We provide quality education with modern facilities and experienced teachers.""",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('School Info created'))

        # Create Contact Info
        contact_info = ContactInfo.objects.create(
            page_title="Contact Us",
            page_title_bn="যোগাযোগ করুন",
            page_subtitle="Get in touch with us for any inquiries",
            page_subtitle_bn="যে কোন তথ্যের জন্য যোগাযোগ করুন",
            address="123 School Road, Noagaon, Bangladesh",
            address_bn="১২৩ স্কুল রোড, নোয়াগাঁও, বাংলাদেশ",
            main_phone="+880 1234-567890",
            admissions_phone="+880 1234-567891",
            general_email="info@noagaonhighschool.edu.bd",
            admissions_email="admissions@noagaonhighschool.edu.bd",
            office_hours="Sunday - Thursday: 8:00 AM - 4:00 PM",
            office_hours_bn="রবিবার - বৃহস্পতিবার: সকাল ৮:০০ - বিকাল ৪:০০",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('Contact Info created'))

        # Create Headmaster
        headmaster = Headmaster.objects.create(
            name="Dr. Abdul Karim",
            qualification="Ph.D. in Education",
            experience_years=25,
            contact_info="headmaster@noagaonhighschool.edu.bd",
            bio="Dr. Abdul Karim has been serving in education for over 25 years.",
            message="Welcome to Noagaon High School. Our mission is to provide quality education.",
            achievements="Multiple awards in educational leadership",
            education="Ph.D. in Education, M.Ed, B.Ed",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('Headmaster created'))

        # Create Teachers
        teachers = [
            {"name": "Md. Rafiqul Islam", "subject": "Mathematics", "designation": "Senior Teacher"},
            {"name": "Fatima Begum", "subject": "Bengali", "designation": "Senior Teacher"},
            {"name": "Mohammad Ali", "subject": "English", "designation": "Assistant Teacher"},
            {"name": "Nasrin Akter", "subject": "Science", "designation": "Assistant Teacher"},
            {"name": "Kamal Hossain", "subject": "Social Studies", "designation": "Teacher"}
        ]
        for teacher_data in teachers:
            Teacher.objects.create(**teacher_data)
        self.stdout.write(self.style.SUCCESS('Teachers created'))

        # Create Committee Members
        committee_members = [
            {"name": "Abdur Rahman", "role": "President", "order": 1},
            {"name": "Shahida Begum", "role": "Vice President", "order": 2},
            {"name": "Mohammad Hossain", "role": "Secretary", "order": 3},
            {"name": "Nasima Khatun", "role": "Treasurer", "order": 4},
            {"name": "Abdul Malik", "role": "Member", "order": 5}
        ]
        for member_data in committee_members:
            CommitteeMember.objects.create(**member_data)
        self.stdout.write(self.style.SUCCESS('Committee Members created'))

        # Create Exam Types
        exam_types = [
            {"name": "First Term", "code": "first_term", "order": 1},
            {"name": "Second Term", "code": "second_term", "order": 2},
            {"name": "Final", "code": "final", "order": 3},
            {"name": "Test", "code": "test", "order": 4},
            {"name": "Annual", "code": "annual", "order": 5}
        ]
        for exam_type_data in exam_types:
            ExamType.objects.create(**exam_type_data)
        self.stdout.write(self.style.SUCCESS('Exam Types created'))

        # Create Student Classes
        classes = [
            {"name": "Class 6", "code": "6", "order": 1},
            {"name": "Class 7", "code": "7", "order": 2},
            {"name": "Class 8", "code": "8", "order": 3},
            {"name": "Class 9", "code": "9", "order": 4},
            {"name": "Class 10", "code": "10", "order": 5}
        ]
        for class_data in classes:
            StudentClass.objects.create(**class_data)
        self.stdout.write(self.style.SUCCESS('Student Classes created'))

        # Create Gallery Categories
        categories = [
            {"name": "School Events", "description": "Photos from various school events"},
            {"name": "Sports", "description": "Sports activities and competitions"},
            {"name": "Cultural Programs", "description": "Cultural events and celebrations"},
            {"name": "Academic Activities", "description": "Classroom and academic activities"},
            {"name": "Achievement", "description": "Student and school achievements"}
        ]
        for category_data in categories:
            GalleryCategory.objects.create(**category_data)
        self.stdout.write(self.style.SUCCESS('Gallery Categories created'))

        # Create Navigation Links
        nav_links = [
            {
                "title": "Home",
                "title_bn": "হোম",
                "link_type": "internal",
                "internal_page": "main:home",
                "position": "main",
                "order": 1,
                "icon_class": "fas fa-home"
            },
            {
                "title": "Notices",
                "title_bn": "নোটিশ",
                "link_type": "internal",
                "internal_page": "main:notices",
                "position": "main",
                "order": 2,
                "icon_class": "fas fa-bell"
            },
            {
                "title": "Results",
                "title_bn": "ফলাফল",
                "link_type": "internal",
                "internal_page": "main:exam_results",
                "position": "important",
                "order": 1,
                "icon_class": "fas fa-graduation-cap"
            }
        ]
        for link_data in nav_links:
            NavigationLink.objects.create(**link_data)
        self.stdout.write(self.style.SUCCESS('Navigation Links created'))

        # Create Students (sample data for Class 6)
        class_6 = StudentClass.objects.get(code="6")
        sections = ['A', 'B', 'C']
        for i in range(1, 31):  # Create 30 students
            section = random.choice(sections)
            Student.objects.create(
                name=f"Student {i}",
                roll_number=f"{i:02d}",
                class_name="6",
                section=section,
                gender=random.choice(['male', 'female']),
                admission_date=timezone.now().date() - timedelta(days=random.randint(1, 365)),
                is_active=True
            )
        self.stdout.write(self.style.SUCCESS('Students created'))

        # Create Notices
        admin_user = User.objects.get(username='admin')
        notices = [
            {
                "title": "Annual Sports Day 2025",
                "notice_type": "text",
                "content": "Annual Sports Day will be held on September 15, 2025.",
                "is_important": True,
                "created_by": admin_user
            },
            {
                "title": "Parent-Teacher Meeting",
                "notice_type": "text",
                "content": "Parent-Teacher meeting scheduled for August 30, 2025.",
                "is_important": False,
                "created_by": admin_user
            }
        ]
        for notice_data in notices:
            Notice.objects.create(**notice_data)
        self.stdout.write(self.style.SUCCESS('Notices created'))

        # Create Exam Results
        exam_types = ExamType.objects.all()
        classes = StudentClass.objects.all()
        for exam_type in exam_types[:2]:  # Create results for first two exam types
            for student_class in classes[:2]:  # Create results for first two classes
                ExamResult.objects.create(
                    title=f"{exam_type.name} Examination 2025 - {student_class.name}",
                    student_class=student_class,
                    exam_type=exam_type,
                    result_type="text",
                    text_content=f"Sample result content for {student_class.name} {exam_type.name}",
                    exam_date=timezone.now().date() - timedelta(days=30),
                    result_publish_date=timezone.now().date() - timedelta(days=15),
                    description=f"Examination results for {student_class.name} {exam_type.name}",
                    is_published=True,
                    uploaded_by=admin_user
                )
        self.stdout.write(self.style.SUCCESS('Exam Results created'))

        self.stdout.write(self.style.SUCCESS('Successfully populated demo data'))
