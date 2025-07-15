import os
from django.conf import settings


def school_info(request):
    """
    Context processor to provide school information globally
    """
    # Try to get school info from database first
    try:
        from .models import SchoolInfo
        school = SchoolInfo.objects.filter(is_active=True).first()

        if school:
            return {
                'school_name': school.name,
                'school_logo': school.logo.url if school.logo else get_default_logo(),
                'school_tagline': school.tagline,
                'school_address': school.address,
                'school_phone': school.phone,
                'school_email': school.email,
                'school_website': school.website,
                'school_established': school.established_year,
                'school_about': school.about,
            }
    except:
        pass

    # Fallback to default values
    return {
        'school_name': 'Noagaon High School',
        'school_logo': get_default_logo(),
        'school_tagline': 'Excellence in Education Since 1950',
        'school_address': '',
        'school_phone': '',
        'school_email': '',
        'school_website': '',
        'school_established': 1950,
        'school_about': '',
    }


def get_default_logo():
    """Get the default logo URL"""
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo', 'Noagaon_logo.jpg')
    if os.path.exists(logo_path):
        return f"{settings.MEDIA_URL}logo/Noagaon_logo.jpg"
    return None
