import os
from django.conf import settings


def school_info(request):
    """
    Context processor to provide school information globally
    """
    context = {}

    # Try to get school info from database first
    try:
        from .models import SchoolInfo, NavigationLink
        school = SchoolInfo.objects.filter(is_active=True).first()

        if school:
            context.update({
                'school_name': school.name,
                'school_logo': school.logo.url if school.logo else get_default_logo(),
                'school_tagline': school.tagline,
                'school_address': school.address,
                'school_phone': school.phone,
                'school_email': school.email,
                'school_website': school.website,
                'school_established': school.established_year,
                'school_about': school.about,
            })
        else:
            # Fallback to default values
            context.update({
                'school_name': 'Noagaon High School',
                'school_logo': get_default_logo(),
                'school_tagline': 'Excellence in Education Since 1950',
                'school_address': '',
                'school_phone': '',
                'school_email': '',
                'school_website': '',
                'school_established': 1950,
                'school_about': '',
            })

        # Get navigation links
        main_nav_links = NavigationLink.objects.filter(
            position='main', is_active=True
        ).order_by('order')

        important_links = NavigationLink.objects.filter(
            position='important', is_active=True
        ).order_by('order')

        footer_links = NavigationLink.objects.filter(
            position='footer', is_active=True
        ).order_by('order')

        context.update({
            'main_nav_links': main_nav_links,
            'important_links': important_links,
            'footer_links': footer_links,
        })

    except Exception as e:
        # Fallback to default values if there's any error
        context.update({
            'school_name': 'Noagaon High School',
            'school_logo': get_default_logo(),
            'school_tagline': 'Excellence in Education Since 1950',
            'school_address': '',
            'school_phone': '',
            'school_email': '',
            'school_website': '',
            'school_established': 1950,
            'school_about': '',
            'main_nav_links': [],
            'important_links': [],
            'footer_links': [],
        })

    return context


def get_default_logo():
    """Get the default logo URL"""
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo', 'Noagaon_logo.jpg')
    if os.path.exists(logo_path):
        return f"{settings.MEDIA_URL}logo/Noagaon_logo.jpg"
    return None
