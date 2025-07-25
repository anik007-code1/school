from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import Notice, Teacher, CommitteeMember, Headmaster, GalleryCategory, GalleryImage


def home(request):
    """Homepage view"""
    latest_notices = Notice.objects.all()[:3]  # Show latest 3 notices

    # Debug: Print current language
    current_language = translation.get_language()
    print(f"Current language: {current_language}")

    context = {
        'latest_notices': latest_notices,
    }
    return render(request, 'main/home.html', context)


def notices(request):
    """Notices list view with pagination"""
    notices_list = Notice.objects.all()
    paginator = Paginator(notices_list, 10)  # Show 10 notices per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main/notices.html', context)


def teachers(request):
    """Teachers list view with pagination"""
    teachers_list = Teacher.objects.all()
    paginator = Paginator(teachers_list, 8)  # Show 8 teachers per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main/teachers.html', context)


def committee(request):
    """Managing committee view"""
    committee_members = CommitteeMember.objects.all()
    context = {
        'committee_members': committee_members,
    }
    return render(request, 'main/committee.html', context)


def contact(request):
    """Contact page view"""
    return render(request, 'main/contact.html')


def headmaster(request):
    """Headmaster page view"""
    try:
        headmaster_info = Headmaster.objects.filter(is_active=True).first()
    except Headmaster.DoesNotExist:
        headmaster_info = None

    context = {
        'headmaster': headmaster_info,
    }
    return render(request, 'main/headmaster.html', context)


def notice_detail(request, notice_id):
    """Individual notice detail view"""
    notice = get_object_or_404(Notice, id=notice_id)
    context = {
        'notice': notice,
    }
    return render(request, 'main/notice_detail.html', context)


def gallery(request):
    """Gallery view with pagination and category filtering"""
    category_id = request.GET.get('category')
    categories = GalleryCategory.objects.filter(is_active=True)

    if category_id:
        images_list = GalleryImage.objects.filter(category_id=category_id)
        selected_category = get_object_or_404(GalleryCategory, id=category_id, is_active=True)
    else:
        images_list = GalleryImage.objects.all()
        selected_category = None

    paginator = Paginator(images_list, 12)  # Show 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'main/gallery.html', context)


def gallery_image_detail(request, image_id):
    """Individual gallery image detail view"""
    image = get_object_or_404(GalleryImage, id=image_id)

    # Get previous and next images in the same category
    category_images = GalleryImage.objects.filter(category=image.category).order_by('order', '-upload_date')
    image_ids = list(category_images.values_list('id', flat=True))

    try:
        current_index = image_ids.index(image.id)
        prev_image_id = image_ids[current_index - 1] if current_index > 0 else None
        next_image_id = image_ids[current_index + 1] if current_index < len(image_ids) - 1 else None
    except ValueError:
        prev_image_id = next_image_id = None

    context = {
        'image': image,
        'prev_image_id': prev_image_id,
        'next_image_id': next_image_id,
    }
    return render(request, 'main/gallery_detail.html', context)


def switch_language(request, language_code):
    """Custom language switcher view"""
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if language_code in [lang[0] for lang in settings.LANGUAGES]:
        if hasattr(request, 'session'):
            request.session['django_language'] = language_code
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
        translation.activate(language_code)

    return response
