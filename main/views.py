from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import Count, Q
from .models import (Notice, Teacher, CommitteeMember, Headmaster, GalleryCategory,
                     GalleryImage, ContactInfo, ExamResult, HomepageSlider, ClasswiseStudentCount)


def home(request):
    """Homepage view with slider"""
    latest_notices = Notice.objects.all()[:3]  # Show latest 3 notices
    slider_images = HomepageSlider.objects.filter(is_active=True).order_by('order')[:5]  # Show max 5 slides
    
    context = {
        'latest_notices': latest_notices,
        'slider_images': slider_images,
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
    try:
        contact_info = ContactInfo.objects.filter(is_active=True).first()
    except ContactInfo.DoesNotExist:
        contact_info = None

    context = {
        'contact_info': contact_info,
    }
    return render(request, 'main/contact.html', context)


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


def students(request):
    """Students statistics view"""
    # Get the latest academic year's data
    current_year = 2025  # You might want to make this dynamic
    class_stats = ClasswiseStudentCount.objects.filter(academic_year=current_year)
    
    # Calculate total statistics
    total_students = sum(stat.total_students for stat in class_stats)
    male_students = sum(stat.total_male for stat in class_stats)
    female_students = sum(stat.total_female for stat in class_stats)
    
    # Prepare class-wise data
    class_stats_data = [
        {
            'class_name': stat.student_class.name,
            'total': stat.total_students,
            'male': stat.total_male,
            'female': stat.total_female
        }
        for stat in class_stats
    ]
    
    context = {
        'total_students': total_students,
        'male_students': male_students,
        'female_students': female_students,
        'class_stats': class_stats_data
    }
    return render(request, 'main/students.html', context)


def exam_results(request):
    """Exam results view with class filtering"""
    class_filter = request.GET.get('class')
    exam_type_filter = request.GET.get('exam_type')
    
    # Get published results
    results_list = ExamResult.objects.filter(is_published=True)
    
    # Apply filters
    if class_filter:
        results_list = results_list.filter(student_class__code=class_filter)
    if exam_type_filter:
        results_list = results_list.filter(exam_type__code=exam_type_filter)
    
    # Pagination
    paginator = Paginator(results_list, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get available classes and exam types for filtering
    available_classes = ExamResult.objects.filter(is_published=True).values_list(
        'student_class__code', 'student_class__name').distinct().order_by('student_class__code')
    available_exam_types = ExamResult.objects.filter(is_published=True).values_list(
        'exam_type__code', 'exam_type__name').distinct()
    
    context = {
        'page_obj': page_obj,
        'available_classes': available_classes,
        'available_exam_types': available_exam_types,
        'current_class': class_filter,
        'current_exam_type': exam_type_filter,
    }
    return render(request, 'main/exam_results.html', context)


def exam_result_detail(request, result_id):
    """Individual exam result detail view"""
    result = get_object_or_404(ExamResult, id=result_id, is_published=True)
    context = {
        'result': result,
    }
    return render(request, 'main/exam_result_detail.html', context)
