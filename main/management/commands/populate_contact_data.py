from django.core.management.base import BaseCommand
from main.models import ContactInfo


class Command(BaseCommand):
    help = 'Populate sample contact information'

    def handle(self, *args, **options):
        # Create sample contact information
        contact_info, created = ContactInfo.objects.get_or_create(
            defaults={
                'page_title': 'Contact Us',
                'page_title_bn': 'যোগাযোগ করুন',
                'page_subtitle': 'Get in touch with us for any inquiries or information',
                'page_subtitle_bn': 'যেকোনো জিজ্ঞাসা বা তথ্যের জন্য আমাদের সাথে যোগাযোগ করুন',
                'address': '''Noagaon High School
Village: Noagaon
Post Office: Noagaon
Upazila: Daudkandi
District: Cumilla
Bangladesh - 3516''',
                'address_bn': '''নোয়াগাঁও উচ্চ বিদ্যালয়
গ্রাম: নোয়াগাঁও
ডাকঘর: নোয়াগাঁও
উপজেলা: দাউদকান্দি
জেলা: কুমিল্লা
বাংলাদেশ - ৩৫১৬''',
                'main_phone': '+880-1234-567890',
                'admissions_phone': '+880-1234-567891',
                'additional_phone': '+880-1234-567892',
                'general_email': 'info@noagaonhighschool.edu.bd',
                'admissions_email': 'admissions@noagaonhighschool.edu.bd',
                'office_hours': '''Saturday - Thursday: 9:00 AM - 5:00 PM
Friday: Closed
Lunch Break: 1:00 PM - 2:00 PM''',
                'office_hours_bn': '''শনিবার - বৃহস্পতিবার: সকাল ৯:০০ - বিকাল ৫:০০
শুক্রবার: বন্ধ
দুপুরের বিরতি: দুপুর ১:০০ - দুপুর ২:০০''',
                'enable_contact_form': True,
                'form_title': 'Send us a Message',
                'form_title_bn': 'আমাদের একটি বার্তা পাঠান',
                'additional_info': '''For urgent matters, please call our main office number.
For admission-related queries, please contact our admissions office.
We welcome visitors during office hours.''',
                'additional_info_bn': '''জরুরি বিষয়ের জন্য, অনুগ্রহ করে আমাদের প্রধান অফিস নম্বরে কল করুন।
ভর্তি সংক্রান্ত প্রশ্নের জন্য, অনুগ্রহ করে আমাদের ভর্তি অফিসে যোগাযোগ করুন।
অফিস সময়ে আমরা দর্শনার্থীদের স্বাগত জানাই।''',
                'is_active': True,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created contact information')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Contact information already exists')
            )
