from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Teacher, CommitteeMember, Headmaster, Notice, GalleryCategory, GalleryImage, NavigationLink
from django.core.files.base import ContentFile
import io


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@school.edu',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Create sample teachers
        teachers_data = [
            {
                'name': 'Dr. Sarah Johnson',
                'subject': 'Mathematics',
                'designation': 'Head of Mathematics Department',
                'contact_info': 'sarah.johnson@school.edu',
                'bio': 'Dr. Johnson has been teaching mathematics for over 15 years and holds a PhD in Applied Mathematics.'
            },
            {
                'name': 'Mr. David Wilson',
                'subject': 'English Literature',
                'designation': 'Senior English Teacher',
                'contact_info': 'david.wilson@school.edu',
                'bio': 'Mr. Wilson specializes in contemporary literature and has published several academic papers.'
            },
            {
                'name': 'Ms. Emily Chen',
                'subject': 'Science',
                'designation': 'Science Department Coordinator',
                'contact_info': 'emily.chen@school.edu',
                'bio': 'Ms. Chen teaches both Physics and Chemistry and leads our science fair initiatives.'
            },
            {
                'name': 'Mr. Robert Brown',
                'subject': 'History',
                'designation': 'History Teacher',
                'contact_info': 'robert.brown@school.edu',
                'bio': 'Mr. Brown brings history to life with his engaging teaching methods and extensive knowledge.'
            },
            {
                'name': 'Ms. Lisa Garcia',
                'subject': 'Art',
                'designation': 'Art Teacher',
                'contact_info': 'lisa.garcia@school.edu',
                'bio': 'Ms. Garcia is a professional artist who inspires creativity in all her students.'
            },
            {
                'name': 'Mr. Michael Davis',
                'subject': 'Physical Education',
                'designation': 'PE Teacher & Sports Coordinator',
                'contact_info': 'michael.davis@school.edu',
                'bio': 'Mr. Davis coaches multiple sports teams and promotes healthy living among students.'
            },
            {
                'name': 'Dr. Amanda Taylor',
                'subject': 'Biology',
                'designation': 'Biology Teacher',
                'contact_info': 'amanda.taylor@school.edu',
                'bio': 'Dr. Taylor holds a PhD in Biology and leads our environmental science programs.'
            },
            {
                'name': 'Mr. James Anderson',
                'subject': 'Computer Science',
                'designation': 'IT Coordinator',
                'contact_info': 'james.anderson@school.edu',
                'bio': 'Mr. Anderson teaches programming and manages the school\'s technology infrastructure.'
            },
            {
                'name': 'Ms. Maria Rodriguez',
                'subject': 'Spanish',
                'designation': 'Foreign Language Teacher',
                'contact_info': 'maria.rodriguez@school.edu',
                'bio': 'Ms. Rodriguez is a native Spanish speaker who makes language learning fun and interactive.'
            },
            {
                'name': 'Mr. Thomas White',
                'subject': 'Music',
                'designation': 'Music Teacher & Choir Director',
                'contact_info': 'thomas.white@school.edu',
                'bio': 'Mr. White directs the school choir and teaches various musical instruments.'
            }
        ]
        
        for teacher_data in teachers_data:
            teacher, created = Teacher.objects.get_or_create(
                name=teacher_data['name'],
                defaults=teacher_data
            )
            if created:
                self.stdout.write(f'Created teacher: {teacher.name}')
        
        # Create sample committee members
        committee_data = [
            {
                'name': 'John Smith',
                'role': 'Chairman',
                'contact_info': 'chairman@school.edu',
                'order': 1
            },
            {
                'name': 'Mary Johnson',
                'role': 'Vice Chairman',
                'contact_info': 'vice.chairman@school.edu',
                'order': 2
            },
            {
                'name': 'Robert Davis',
                'role': 'Secretary',
                'contact_info': 'secretary@school.edu',
                'order': 3
            },
            {
                'name': 'Susan Wilson',
                'role': 'Treasurer',
                'contact_info': 'treasurer@school.edu',
                'order': 4
            },
            {
                'name': 'Michael Brown',
                'role': 'Member',
                'contact_info': 'member1@school.edu',
                'order': 5
            },
            {
                'name': 'Jennifer Garcia',
                'role': 'Member',
                'contact_info': 'member2@school.edu',
                'order': 6
            }
        ]
        
        for member_data in committee_data:
            member, created = CommitteeMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Created committee member: {member.name}')

        # Create sample headmaster
        headmaster_data = {
            'name': 'Dr. William Anderson',
            'qualification': 'Ph.D. in Educational Leadership, M.Ed. in School Administration',
            'experience_years': 25,
            'contact_info': 'headmaster@school.edu',
            'bio': '''Dr. William Anderson has been serving as the Headmaster of our school for the past 8 years. With over 25 years of experience in education, he brings a wealth of knowledge and a passion for academic excellence.

Dr. Anderson holds a Ph.D. in Educational Leadership from Harvard University and has previously served as a principal at several prestigious institutions. Under his leadership, our school has achieved remarkable growth in academic performance and student development.

He is known for his innovative approach to education, emphasis on character building, and commitment to creating an inclusive learning environment where every student can thrive.''',
            'message': '''Dear Students, Parents, and Faculty,

Welcome to our school family! As we embark on another academic year, I am filled with excitement about the opportunities that lie ahead. Our school has always been committed to providing not just quality education, but also nurturing young minds to become responsible global citizens.

We believe that education is not just about academic achievement, but about developing character, creativity, and critical thinking skills. Our dedicated faculty works tirelessly to create an environment where every student can discover their potential and pursue their dreams.

I encourage all our students to embrace learning with curiosity and enthusiasm. Remember, success is not just measured by grades, but by the positive impact you make in your community and the world.

Together, let us make this academic year memorable and meaningful.

Warm regards,''',
            'achievements': '''• Led the school to achieve "School of Excellence" status for 3 consecutive years
• Implemented innovative STEM programs that increased student engagement by 40%
• Established partnerships with 5 international schools for student exchange programs
• Received the "Outstanding Educational Leader" award from the State Education Board
• Published research papers on modern teaching methodologies in leading educational journals
• Successfully managed the school's digital transformation during the pandemic
• Increased school enrollment by 35% through strategic planning and community outreach''',
            'education': '''• Ph.D. in Educational Leadership - Harvard University (2005)
• M.Ed. in School Administration - Stanford University (2000)
• B.Ed. in Secondary Education - University of California, Berkeley (1998)
• B.A. in English Literature - Yale University (1996)

Professional Development:
• Certificate in Digital Learning Leadership - MIT (2020)
• Advanced School Management Program - Oxford University (2018)
• Leadership in Educational Innovation - Cambridge University (2015)''',
            'is_active': True
        }

        headmaster, created = Headmaster.objects.get_or_create(
            name=headmaster_data['name'],
            defaults=headmaster_data
        )
        if created:
            self.stdout.write(f'Created headmaster: {headmaster.name}')

        # Create sample notices (both PDF and text types)
        sample_notices = [
            {
                'title': 'School Reopening After Winter Break',
                'notice_type': 'text',
                'content': '''Dear Students and Parents,

We are pleased to announce that the school will reopen on January 8th, 2024, after the winter break.

Important Points:
• Classes will resume with the regular schedule
• All students must bring their completed holiday homework
• New uniforms are available at the school store
• Parent-teacher meetings are scheduled for January 15th

We look forward to welcoming all students back for the new term.

Best regards,
School Administration''',
                'summary': 'School reopens on January 8th, 2024. Students must bring completed holiday homework.',
                'is_important': True,
                'created_by': admin_user
            },
            {
                'title': 'Annual Sports Day 2024',
                'notice_type': 'text',
                'content': '''We are excited to announce our Annual Sports Day 2024!

Date: February 15th, 2024
Time: 9:00 AM - 4:00 PM
Venue: School Sports Ground

Events Include:
• Track and Field Events
• Team Sports (Football, Basketball, Volleyball)
• Fun Games for Junior Students
• Prize Distribution Ceremony

All students are encouraged to participate. Registration forms are available at the sports department.

Parents and guardians are cordially invited to attend and cheer for our young athletes.''',
                'summary': 'Annual Sports Day on February 15th, 2024. Registration forms available at sports department.',
                'is_important': False,
                'created_by': admin_user
            },
            {
                'title': 'Examination Schedule - Final Term',
                'notice_type': 'text',
                'content': '''Final Term Examination Schedule

The final term examinations will be conducted from March 1st to March 15th, 2024.

Examination Guidelines:
• Students must arrive 30 minutes before the exam
• Bring valid ID card and admit card
• Mobile phones are strictly prohibited
• Use only blue/black pen for writing
• Calculators allowed only for Mathematics and Science

Exam Timetable:
• Grade 1-5: March 1st - March 8th
• Grade 6-10: March 8th - March 15th

Detailed timetable will be distributed to all students by February 20th.

Good luck to all students!''',
                'summary': 'Final term exams from March 1-15, 2024. Detailed timetable to be distributed by Feb 20th.',
                'is_important': True,
                'created_by': admin_user
            },
            {
                'title': 'Library New Book Collection',
                'notice_type': 'text',
                'content': '''New Book Collection Available at School Library

We are pleased to inform you that our library has received a new collection of books covering various subjects and genres.

New Additions Include:
• Science and Technology books
• Literature and Fiction
• History and Geography
• Reference books for competitive exams
• Children's story books

Library Timings:
Monday to Friday: 8:00 AM - 4:00 PM
Saturday: 9:00 AM - 1:00 PM

Students can issue up to 3 books at a time for a period of 2 weeks.

Happy Reading!''',
                'summary': 'New book collection available at library. Students can issue up to 3 books for 2 weeks.',
                'is_important': False,
                'created_by': admin_user
            },
            {
                'title': 'Science Fair 2024 - Call for Participation',
                'notice_type': 'text',
                'content': '''Science Fair 2024 - Unleash Your Scientific Creativity!

Date: April 20th, 2024
Theme: "Innovation for a Sustainable Future"

Categories:
• Junior Category (Grades 1-5)
• Senior Category (Grades 6-10)

Project Guidelines:
• Projects can be individual or team-based (max 3 members)
• Focus on environmental sustainability and innovation
• Models, experiments, and research projects are welcome
• Registration deadline: March 30th, 2024

Prizes:
• First Prize: ₹5,000 + Certificate
• Second Prize: ₹3,000 + Certificate
• Third Prize: ₹2,000 + Certificate

For registration and guidelines, contact the Science Department.

Let's make science fun and meaningful!''',
                'summary': 'Science Fair 2024 on April 20th. Theme: Innovation for Sustainable Future. Registration by March 30th.',
                'is_important': False,
                'created_by': admin_user
            }
        ]

        for notice_data in sample_notices:
            notice, created = Notice.objects.get_or_create(
                title=notice_data['title'],
                defaults=notice_data
            )
            if created:
                self.stdout.write(f'Created notice: {notice.title}')

        # Create gallery categories
        gallery_categories = [
            {
                'name': 'School Building',
                'description': 'Images of our school building and infrastructure',
                'order': 1,
                'is_active': True
            },
            {
                'name': 'Classrooms',
                'description': 'Our modern classrooms and learning spaces',
                'order': 2,
                'is_active': True
            },
            {
                'name': 'Sports & Activities',
                'description': 'Sports facilities and extracurricular activities',
                'order': 3,
                'is_active': True
            },
            {
                'name': 'Events & Celebrations',
                'description': 'School events, festivals, and celebrations',
                'order': 4,
                'is_active': True
            },
            {
                'name': 'Library & Labs',
                'description': 'Library, computer labs, and science laboratories',
                'order': 5,
                'is_active': True
            },
            {
                'name': 'Campus Life',
                'description': 'Daily life and activities around the campus',
                'order': 6,
                'is_active': True
            }
        ]

        for category_data in gallery_categories:
            category, created = GalleryCategory.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
            if created:
                self.stdout.write(f'Created gallery category: {category.name}')

        # Create sample navigation links
        navigation_links = [
            # Important Links
            {
                'title': 'Admission Form',
                'title_bn': 'ভর্তির ফরম',
                'link_type': 'external',
                'url': 'https://example.com/admission-form',
                'position': 'important',
                'order': 1,
                'is_active': True,
                'open_new_tab': True,
                'icon_class': 'fas fa-file-alt',
                'description': 'Download admission form for new students'
            },
            {
                'title': 'Academic Calendar',
                'title_bn': 'একাডেমিক ক্যালেন্ডার',
                'link_type': 'external',
                'url': 'https://example.com/academic-calendar',
                'position': 'important',
                'order': 2,
                'is_active': True,
                'open_new_tab': True,
                'icon_class': 'fas fa-calendar',
                'description': 'View academic calendar and important dates'
            },
            {
                'title': 'Online Classes',
                'title_bn': 'অনলাইন ক্লাস',
                'link_type': 'external',
                'url': 'https://meet.google.com',
                'position': 'important',
                'order': 3,
                'is_active': True,
                'open_new_tab': True,
                'icon_class': 'fas fa-video',
                'description': 'Access online classes and virtual meetings'
            },
            {
                'title': 'Student Portal',
                'title_bn': 'শিক্ষার্থী পোর্টাল',
                'link_type': 'external',
                'url': 'https://example.com/student-portal',
                'position': 'important',
                'order': 4,
                'is_active': True,
                'open_new_tab': True,
                'icon_class': 'fas fa-user-graduate',
                'description': 'Student login portal for grades and assignments'
            },

            # Footer Links
            {
                'title': 'Privacy Policy',
                'title_bn': 'গোপনীয়তা নীতি',
                'link_type': 'external',
                'url': 'https://example.com/privacy-policy',
                'position': 'footer',
                'order': 1,
                'is_active': True,
                'open_new_tab': False,
                'icon_class': 'fas fa-shield-alt',
                'description': 'School privacy policy and data protection'
            },
            {
                'title': 'Terms of Service',
                'title_bn': 'সেবার শর্তাবলী',
                'link_type': 'external',
                'url': 'https://example.com/terms-of-service',
                'position': 'footer',
                'order': 2,
                'is_active': True,
                'open_new_tab': False,
                'icon_class': 'fas fa-file-contract',
                'description': 'Terms and conditions for website usage'
            },
            {
                'title': 'School Facebook',
                'title_bn': 'স্কুল ফেসবুক',
                'link_type': 'external',
                'url': 'https://facebook.com/noagaonhighschool',
                'position': 'footer',
                'order': 3,
                'is_active': True,
                'open_new_tab': True,
                'icon_class': 'fab fa-facebook',
                'description': 'Follow us on Facebook for updates'
            },
            {
                'title': 'Contact Form',
                'title_bn': 'যোগাযোগ ফরম',
                'link_type': 'internal',
                'internal_page': 'main:contact',
                'position': 'footer',
                'order': 4,
                'is_active': True,
                'open_new_tab': False,
                'icon_class': 'fas fa-envelope',
                'description': 'Send us a message through contact form'
            }
        ]

        for link_data in navigation_links:
            link, created = NavigationLink.objects.get_or_create(
                title=link_data['title'],
                position=link_data['position'],
                defaults=link_data
            )
            if created:
                self.stdout.write(f'Created navigation link: {link.title} ({link.get_position_display()})')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
