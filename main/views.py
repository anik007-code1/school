from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import (Notice, Teacher, OtherEmployee, CommitteeMember, Headmaster, GalleryCategory,
                     GalleryImage, ContactInfo, ExamResult, HomepageSlider, ExamType, StudentClass, ClasswiseStudentCount)

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


def other_employee(request):
    """Other Employee list view (e.g., cleaners, guards)"""
    staff_list = OtherEmployee.objects.all()
    paginator = Paginator(staff_list, 8)  # Show 8 staff per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main/other_employee.html', context)


def committee(request):
    """Managing committee view"""
    committee_members = CommitteeMember.objects.all()
    context = {
        'committee_members': committee_members,
    }
    return render(request, 'main/committee.html', context)


def headmaster(request):
    """Display headmaster page."""
    headmaster = Headmaster.objects.first()
    context = {
        'headmaster': headmaster,
    }
    return render(request, 'main/headmaster.html', context)


def gallery(request):
    """Display gallery page with categories and images."""
    categories = GalleryCategory.objects.all()
    
    # Get category filter
    category_id = request.GET.get('category')
    selected_category = None
    
    if category_id:
        try:
            selected_category = GalleryCategory.objects.get(id=category_id)
            images = GalleryImage.objects.filter(category=selected_category)
        except GalleryCategory.DoesNotExist:
            images = GalleryImage.objects.all()
    else:
        images = GalleryImage.objects.all()
    
    # Apply pagination
    images = images.order_by('-upload_date')
    paginator = Paginator(images, 12)  # Show 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'page_obj': page_obj,
        'selected_category': selected_category,
    }
    return render(request, 'main/gallery.html', context)


def gallery_image_detail(request, image_id):
    """Display individual gallery image details."""
    image = get_object_or_404(GalleryImage, id=image_id)
    context = {
        'image': image,
    }
    return render(request, 'main/gallery_detail.html', context)


def contact(request):
    """Display contact information page."""
    contact_info = ContactInfo.objects.first()
    context = {
        'contact_info': contact_info,
    }
    return render(request, 'main/contact.html', context)


def students(request):
    """Display students information page."""
    # Get all student counts for the latest academic year
    latest_year = ClasswiseStudentCount.objects.all().order_by('-academic_year').first()
    if latest_year:
        latest_year = latest_year.academic_year
    else:
        latest_year = 2024
    
    student_counts = ClasswiseStudentCount.objects.filter(
        academic_year=latest_year
    ).order_by('student_class__order')
    
    # Handle empty data gracefully
    if not student_counts:
        context = {
            'total_students': 0,
            'male_students': 0,
            'female_students': 0,
            'class_stats': [],
            'no_data': True,
        }
    else:
        # Calculate totals
        total_students = sum(count.total_students for count in student_counts)
        male_students = sum(count.total_male for count in student_counts)
        female_students = sum(count.total_female for count in student_counts)
        
        # Prepare class-wise stats
        class_stats = []
        for count in student_counts:
            class_stats.append({
                'class_name': count.student_class.name,
                'total': count.total_students,
                'male': count.total_male,
                'female': count.total_female
            })
        
        context = {
            'total_students': total_students,
            'male_students': male_students,
            'female_students': female_students,
            'class_stats': class_stats,
            'no_data': False,
        }
    
    return render(request, 'main/students.html', context)


def exam_results(request):
    """Display exam results page with filtering."""
    # Get filter parameters
    class_filter = request.GET.get('class', '')
    exam_type_filter = request.GET.get('exam_type', '')
    
    # Base queryset - only show published results
    results = ExamResult.objects.filter(is_published=True).order_by('-result_publish_date')
    
    # Apply filters
    if class_filter:
        results = results.filter(student_class__code=class_filter)
    if exam_type_filter:
        results = results.filter(exam_type__code=exam_type_filter)
    
    # Pagination
    paginator = Paginator(results, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get available classes and exam types for filters
    available_classes = StudentClass.objects.filter(is_active=True).values_list('code', 'name')
    available_exam_types = ExamType.objects.filter(is_active=True).values_list('code', 'name')
    
    context = {
        'page_obj': page_obj,
        'available_classes': available_classes,
        'available_exam_types': available_exam_types,
        'current_class': class_filter,
        'current_exam_type': exam_type_filter,
    }
    return render(request, 'main/exam_results.html', context)


def exam_result_detail(request, result_id):
    """Display individual exam result details."""
    result = get_object_or_404(ExamResult, id=result_id)
    context = {
        'result': result,
    }
    return render(request, 'main/exam_result_detail.html', context)


def notice_detail(request, notice_id):
    """Individual notice detail view"""
    notice = get_object_or_404(Notice, id=notice_id)
    context = {
        'notice': notice,
    }
    return render(request, 'main/notice_detail.html', context)


def switch_language(request, language_code):
    """Switch the language and redirect back."""
    if language_code in [lang[0] for lang in settings.LANGUAGES]:
        translation.activate(language_code)
        request.session[settings.LANGUAGE_SESSION_KEY] = language_code
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
