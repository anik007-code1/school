from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
import random
from main.models import Student, ExamResult, HomepageSlider


class Command(BaseCommand):
    help = 'Populate sample data for new features (Students, Exam Results, Homepage Slider)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--students',
            type=int,
            default=50,
            help='Number of students to create (default: 50)'
        )
        parser.add_argument(
            '--results',
            type=int,
            default=10,
            help='Number of exam results to create (default: 10)'
        )
        parser.add_argument(
            '--slides',
            type=int,
            default=3,
            help='Number of homepage slides to create (default: 3)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate new features data...'))
        
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@school.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))

        # Create Students
        self.create_students(options['students'])
        
        # Create Exam Results
        self.create_exam_results(options['results'], admin_user)
        
        # Create Homepage Slides
        self.create_homepage_slides(options['slides'], admin_user)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated all new features data!'))

    def create_students(self, count):
        self.stdout.write(f'Creating {count} students...')
        
        # Sample student names
        male_names = [
            'Md. Rahul Ahmed', 'Md. Karim Hassan', 'Md. Arif Rahman', 'Md. Sabbir Hossain',
            'Md. Tanvir Islam', 'Md. Rifat Ali', 'Md. Shakib Khan', 'Md. Rafi Uddin',
            'Md. Nasir Ahmed', 'Md. Fahim Hassan', 'Md. Imran Ali', 'Md. Sohel Rana',
            'Md. Rakib Islam', 'Md. Habib Rahman', 'Md. Sajib Ahmed', 'Md. Tanim Hassan'
        ]
        
        female_names = [
            'Fatema Khatun', 'Rashida Begum', 'Salma Akter', 'Nasreen Sultana',
            'Ruma Khatun', 'Shirina Begum', 'Rehana Akter', 'Kulsum Khatun',
            'Amina Begum', 'Rahima Khatun', 'Shahida Akter', 'Morsheda Begum',
            'Rokeya Khatun', 'Hasina Begum', 'Rashida Akter', 'Salina Khatun'
        ]
        
        father_names = [
            'Md. Abdul Rahman', 'Md. Abdul Karim', 'Md. Abdul Majid', 'Md. Abdul Hamid',
            'Md. Abdul Latif', 'Md. Abdul Mannan', 'Md. Abdul Halim', 'Md. Abdul Aziz'
        ]
        
        mother_names = [
            'Rashida Begum', 'Fatema Khatun', 'Salma Begum', 'Nasreen Khatun',
            'Ruma Begum', 'Shirina Khatun', 'Rehana Begum', 'Kulsum Khatun'
        ]
        
        classes = ['6', '7', '8', '9', '10']
        sections = ['A', 'B', 'C']
        
        students_created = 0
        
        for i in range(count):
            gender = random.choice(['male', 'female'])
            class_name = random.choice(classes)
            section = random.choice(sections)
            
            # Generate roll number
            roll_number = f"{class_name}{section}{str(i+1).zfill(3)}"
            
            # Check if student already exists
            if Student.objects.filter(roll_number=roll_number, class_name=class_name, section=section).exists():
                continue
            
            name = random.choice(male_names if gender == 'male' else female_names)
            
            student = Student.objects.create(
                name=name,
                roll_number=roll_number,
                class_name=class_name,
                section=section,
                gender=gender,
                admission_date=date.today() - timedelta(days=random.randint(30, 365)),
                father_name=random.choice(father_names),
                mother_name=random.choice(mother_names),
                guardian_phone=f"01{random.randint(700000000, 999999999)}",
                address=f"Village: {random.choice(['Noagaon', 'Rampur', 'Karimpur', 'Islampur'])}, "
                        f"Post: {random.choice(['Noagaon', 'Rampur', 'Karimpur'])}, "
                        f"Upazila: {random.choice(['Sadar', 'Kotchandpur', 'Maheshpur'])}, "
                        f"District: Jhenaidah",
                is_active=random.choice([True, True, True, False])  # 75% active
            )
            students_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {students_created} students'))

    def create_exam_results(self, count, admin_user):
        self.stdout.write(f'Creating {count} exam results...')
        
        classes = ['6', '7', '8', '9', '10']
        exam_types = ['first_term', 'second_term', 'final', 'test', 'annual']
        result_types = ['pdf', 'image']
        
        exam_titles = [
            'First Term Examination 2024',
            'Second Term Examination 2024',
            'Final Examination 2024',
            'Test Examination 2024',
            'Annual Examination 2024',
            'Half Yearly Examination 2024',
            'Pre-Test Examination 2024',
            'Model Test 2024'
        ]
        
        descriptions = [
            'This examination was conducted to evaluate student performance in the current academic session.',
            'Students are advised to check their results carefully and contact the office for any discrepancies.',
            'The examination covered all subjects taught during the term with comprehensive question patterns.',
            'Results are published based on the evaluation of answer scripts by qualified teachers.',
            'Students who have failed in any subject can apply for re-examination within the specified time.',
        ]
        
        results_created = 0
        
        for i in range(count):
            class_name = random.choice(classes)
            exam_type = random.choice(exam_types)
            result_type = random.choice(result_types)
            
            title = f"{random.choice(exam_titles)} - Class {class_name}"
            
            # Generate exam date (within last 6 months)
            exam_date = date.today() - timedelta(days=random.randint(30, 180))
            result_publish_date = exam_date + timedelta(days=random.randint(15, 45))
            
            exam_result = ExamResult.objects.create(
                title=title,
                class_name=class_name,
                exam_type=exam_type,
                result_type=result_type,
                exam_date=exam_date,
                result_publish_date=result_publish_date,
                description=random.choice(descriptions),
                is_published=random.choice([True, True, False]),  # 66% published
                uploaded_by=admin_user
            )
            results_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {results_created} exam results'))
        self.stdout.write(self.style.WARNING('Note: Result files need to be uploaded manually through admin panel'))

    def create_homepage_slides(self, count, admin_user):
        self.stdout.write(f'Creating {count} homepage slides...')
        
        slide_data = [
            {
                'title': 'Welcome to Noagaon High School',
                'subtitle': 'Excellence in Education Since 1950',
                'caption': 'Nurturing young minds to become responsible citizens and future leaders of our nation.',
                'link_text': 'Learn More',
                'link_url': '/about/',
            },
            {
                'title': 'Quality Education for All',
                'subtitle': 'Modern Facilities & Dedicated Teachers',
                'caption': 'We provide comprehensive education with state-of-the-art facilities and experienced faculty.',
                'link_text': 'View Facilities',
                'link_url': '/gallery/',
            },
            {
                'title': 'Join Our School Community',
                'subtitle': 'Admissions Open for Academic Year 2024-25',
                'caption': 'Enroll your child in our school and give them the best foundation for their future.',
                'link_text': 'Apply Now',
                'link_url': '/contact/',
            },
            {
                'title': 'Academic Excellence',
                'subtitle': 'Outstanding Results Year After Year',
                'caption': 'Our students consistently achieve excellent results in board examinations and competitions.',
                'link_text': 'View Results',
                'link_url': '/exam-results/',
            },
            {
                'title': 'Extracurricular Activities',
                'subtitle': 'Sports, Arts & Cultural Programs',
                'caption': 'We believe in holistic development through various sports and cultural activities.',
                'link_text': 'View Gallery',
                'link_url': '/gallery/',
            }
        ]
        
        slides_created = 0
        
        for i in range(min(count, len(slide_data))):
            data = slide_data[i]
            
            slide = HomepageSlider.objects.create(
                title=data['title'],
                subtitle=data['subtitle'],
                caption=data['caption'],
                link_text=data['link_text'],
                link_url=data['link_url'],
                order=i + 1,
                is_active=True,
                created_by=admin_user
            )
            slides_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {slides_created} homepage slides'))
        self.stdout.write(self.style.WARNING('Note: Slide images need to be uploaded manually through admin panel'))