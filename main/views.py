from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import Count, Q
from .models import (Notice, Teacher, OtherEmployee, CommitteeMember, Headmaster, GalleryCategory,
                     GalleryImage, ContactInfo, ExamResult, HomepageSlider, ExamType, StudentClass, ClasswiseStudentCount)
from .forms import (NoticeForm, TeacherForm, OtherEmployeeForm, CommitteeMemberForm, HeadmasterForm,
                    GalleryCategoryForm, GalleryImageForm, ContactInfoForm, ExamResultForm,
                    HomepageSliderForm, ExamTypeForm, StudentClassForm, ClasswiseStudentCountForm)
from .decorators import superuser_required


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
    headmasters = Headmaster.objects.all()
    context = {
        'headmasters': headmasters,
    }
    return render(request, 'main/headmaster.html', context)


# Custom Admin Panel
@superuser_required
def custom_admin(request):
    """Simple custom admin dashboard"""
    stats = {
        'total_notices': Notice.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_other_employees': OtherEmployee.objects.count(),
        'total_committee_members': CommitteeMember.objects.count(),
        'total_exam_results': ExamResult.objects.count(),
        'total_slides': HomepageSlider.objects.count(),
    }
    return render(request, 'main/custom_admin/dashboard.html', {'stats': stats})

def notice_detail(request, notice_id):
    """Individual notice detail view"""
    notice = get_object_or_404(Notice, id=notice_id)
    context = {
        'notice': notice,
    }
    return render(request, 'main/notice_detail.html', context)


# Notice Management
@superuser_required
def notice_list(request):
    notices = Notice.objects.all().order_by('-upload_date')
    return render(request, 'main/custom_admin/notice_list.html', {'notices': notices})


@superuser_required
def notice_add(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            messages.success(request, 'Notice added successfully!')
            return redirect('main:notice_list')
    else:
        form = NoticeForm()
    return render(request, 'main/custom_admin/notice_form.html', {'form': form})


@superuser_required
def notice_edit(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully!')
            return redirect('main:notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'main/custom_admin/notice_form.html', {'form': form, 'notice': notice})


@superuser_required
def notice_delete(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('main:notice_list')
    return render(request, 'main/custom_admin/notice_confirm_delete.html', {'notice': notice})


# Teacher Management
@superuser_required
def teacher_list(request):
    teachers = Teacher.objects.all().order_by('name')
    return render(request, 'main/custom_admin/teacher_list.html', {'teachers': teachers})


@superuser_required
def teacher_add(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully!')
            return redirect('main:teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'main/custom_admin/teacher_form.html', {'form': form})


@superuser_required
def teacher_edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully!')
            return redirect('main:teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'main/custom_admin/teacher_form.html', {'form': form, 'teacher': teacher})


@superuser_required
def teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('main:teacher_list')
    return render(request, 'main/custom_admin/teacher_confirm_delete.html', {'teacher': teacher})


# Other Employee Management
@superuser_required
def other_employee_list(request):
    employees = OtherEmployee.objects.all().order_by('name')
    return render(request, 'main/custom_admin/other_employee_list.html', {'employees': employees})


@superuser_required
def other_employee_add(request):
    if request.method == 'POST':
        form = OtherEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('main:other_employee_list')
    else:
        form = OtherEmployeeForm()
    return render(request, 'main/custom_admin/other_employee_form.html', {'form': form})


@superuser_required
def other_employee_edit(request, employee_id):
    employee = get_object_or_404(OtherEmployee, id=employee_id)
    if request.method == 'POST':
        form = OtherEmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('main:other_employee_list')
    else:
        form = OtherEmployeeForm(instance=employee)
    return render(request, 'main/custom_admin/other_employee_form.html', {'form': form, 'employee': employee})


@superuser_required
def other_employee_delete(request, employee_id):
    employee = get_object_or_404(OtherEmployee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('main:other_employee_list')
    return render(request, 'main/custom_admin/other_employee_confirm_delete.html', {'employee': employee})


# Exam Result Management
@superuser_required
def exam_result_list(request):
    results = ExamResult.objects.all().order_by('-result_publish_date')
    return render(request, 'main/custom_admin/exam_result_list.html', {'results': results})


@superuser_required
def exam_result_add(request):
    if request.method == 'POST':
        form = ExamResultForm(request.POST, request.FILES)
        if form.is_valid():
            result = form.save(commit=False)
            result.uploaded_by = request.user
            result.save()
            messages.success(request, 'Exam result added successfully!')
            return redirect('main:exam_result_list')
    else:
        form = ExamResultForm()
    return render(request, 'main/custom_admin/exam_result_form.html', {'form': form})


@superuser_required
def exam_result_edit(request, result_id):
    result = get_object_or_404(ExamResult, id=result_id)
    if request.method == 'POST':
        form = ExamResultForm(request.POST, request.FILES, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam result updated successfully!')
            return redirect('main:exam_result_list')
    else:
        form = ExamResultForm(instance=result)
    return render(request, 'main/custom_admin/exam_result_form.html', {'form': form, 'result': result})


@superuser_required
def exam_result_delete(request, result_id):
    result = get_object_or_404(ExamResult, id=result_id)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Exam result deleted successfully!')
        return redirect('main:exam_result_list')
    return render(request, 'main/custom_admin/exam_result_confirm_delete.html', {'result': result})


# Committee Member Management
@superuser_required
def committee_member_list(request):
    members = CommitteeMember.objects.all().order_by('order', 'name')
    return render(request, 'main/custom_admin/committee_member_list.html', {'members': members})


@superuser_required
def committee_member_add(request):
    if request.method == 'POST':
        form = CommitteeMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Committee member added successfully!')
            return redirect('main:committee_member_list')
    else:
        form = CommitteeMemberForm()
    return render(request, 'main/custom_admin/committee_member_form.html', {'form': form})


@superuser_required
def committee_member_edit(request, member_id):
    member = get_object_or_404(CommitteeMember, id=member_id)
    if request.method == 'POST':
        form = CommitteeMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Committee member updated successfully!')
            return redirect('main:committee_member_list')
    else:
        form = CommitteeMemberForm(instance=member)
    return render(request, 'main/custom_admin/committee_member_form.html', {'form': form, 'member': member})


@superuser_required
def committee_member_delete(request, member_id):
    member = get_object_or_404(CommitteeMember, id=member_id)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Committee member deleted successfully!')
        return redirect('main:committee_member_list')
    return render(request, 'main/custom_admin/committee_member_confirm_delete.html', {'member': member})


# Headmaster Management
@superuser_required
def headmaster_list(request):
    headmasters = Headmaster.objects.all().order_by('-is_active', 'name')
    return render(request, 'main/custom_admin/headmaster_list.html', {'headmasters': headmasters})


@superuser_required
def headmaster_add(request):
    if request.method == 'POST':
        form = HeadmasterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Headmaster added successfully!')
            return redirect('main:headmaster_list')
    else:
        form = HeadmasterForm()
    return render(request, 'main/custom_admin/headmaster_form.html', {'form': form})


@superuser_required
def headmaster_edit(request, headmaster_id):
    headmaster = get_object_or_404(Headmaster, id=headmaster_id)
    if request.method == 'POST':
        form = HeadmasterForm(request.POST, request.FILES, instance=headmaster)
        if form.is_valid():
            form.save()
            messages.success(request, 'Headmaster updated successfully!')
            return redirect('main:headmaster_list')
    else:
        form = HeadmasterForm(instance=headmaster)
    return render(request, 'main/custom_admin/headmaster_form.html', {'form': form, 'headmaster': headmaster})


def gallery(request):
    """Display gallery page with categories and images."""
    categories = GalleryCategory.objects.all()
    images = GalleryImage.objects.all().order_by('-upload_date')[:12]  # Show latest 12 images
    
    context = {
        'categories': categories,
        'images': images,
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


def switch_language(request, language_code):
    """Switch the language and redirect back."""
    if language_code in [lang[0] for lang in settings.LANGUAGES]:
        translation.activate(language_code)
        request.session[settings.LANGUAGE_SESSION_KEY] = language_code
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@superuser_required
def headmaster_delete(request, headmaster_id):
    headmaster = get_object_or_404(Headmaster, id=headmaster_id)
    if request.method == 'POST':
        headmaster.delete()
        messages.success(request, 'Headmaster deleted successfully!')
        return redirect('main:headmaster_list')
    return render(request, 'main/custom_admin/headmaster_confirm_delete.html', {'headmaster': headmaster})


# Homepage Slider Management
@superuser_required
def slider_list(request):
    sliders = HomepageSlider.objects.all().order_by('order')
    return render(request, 'main/custom_admin/slider_list.html', {'sliders': sliders})

@superuser_required
def slider_add(request):
    if request.method == 'POST':
        form = HomepageSliderForm(request.POST, request.FILES)
        if form.is_valid():
            slider = form.save(commit=False)
            slider.created_by = request.user
            slider.save()
            messages.success(request, 'Slider added successfully!')
            return redirect('main:slider_list')
    else:
        form = HomepageSliderForm()
    return render(request, 'main/custom_admin/slider_form.html', {'form': form})

@superuser_required
def slider_edit(request, slider_id):
    slider = get_object_or_404(HomepageSlider, id=slider_id)
    if request.method == 'POST':
        form = HomepageSliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider updated successfully!')
            return redirect('main:slider_list')
    else:
        form = HomepageSliderForm(instance=slider)
    return render(request, 'main/custom_admin/slider_form.html', {'form': form, 'slider': slider})

@superuser_required
def slider_delete(request, slider_id):
    slider = get_object_or_404(HomepageSlider, id=slider_id)
    if request.method == 'POST':
        slider.delete()
        messages.success(request, 'Slider deleted successfully!')
        return redirect('main:slider_list')
    return render(request, 'main/custom_admin/slider_confirm_delete.html', {'slider': slider})


# Gallery Category Management
@superuser_required
def gallery_category_list(request):
    categories = GalleryCategory.objects.all().order_by('order', 'name')
    return render(request, 'main/custom_admin/gallery_category_list.html', {'categories': categories})

@superuser_required
def gallery_category_add(request):
    if request.method == 'POST':
        form = GalleryCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery category added successfully!')
            return redirect('main:gallery_category_list')
    else:
        form = GalleryCategoryForm()
    return render(request, 'main/custom_admin/gallery_category_form.html', {'form': form})

@superuser_required
def gallery_category_edit(request, category_id):
    category = get_object_or_404(GalleryCategory, id=category_id)
    if request.method == 'POST':
        form = GalleryCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery category updated successfully!')
            return redirect('main:gallery_category_list')
    else:
        form = GalleryCategoryForm(instance=category)
    return render(request, 'main/custom_admin/gallery_category_form.html', {'form': form, 'category': category})

@superuser_required
def gallery_category_delete(request, category_id):
    category = get_object_or_404(GalleryCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Gallery category deleted successfully!')
        return redirect('main:gallery_category_list')
    return render(request, 'main/custom_admin/gallery_category_confirm_delete.html', {'category': category})


# Gallery Image Management
@superuser_required
def gallery_image_list(request):
    images = GalleryImage.objects.all().order_by('-upload_date')
    return render(request, 'main/custom_admin/gallery_image_list.html', {'images': images})

@superuser_required
def gallery_image_add(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            image.save()
            messages.success(request, 'Gallery image added successfully!')
            return redirect('main:gallery_image_list')
    else:
        form = GalleryImageForm()
    return render(request, 'main/custom_admin/gallery_image_form.html', {'form': form})

@superuser_required
def gallery_image_edit(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery image updated successfully!')
            return redirect('main:gallery_image_list')
    else:
        form = GalleryImageForm(instance=image)
    return render(request, 'main/custom_admin/gallery_image_form.html', {'form': form, 'image': image})

@superuser_required
def gallery_image_delete(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Gallery image deleted successfully!')
        return redirect('main:gallery_image_list')
    return render(request, 'main/custom_admin/gallery_image_confirm_delete.html', {'image': image})


# School Info Management
@superuser_required
def school_info_list(request):
    infos = SchoolInfo.objects.all().order_by('-is_active', 'name')
    return render(request, 'main/custom_admin/school_info_list.html', {'infos': infos})

@superuser_required
def school_info_add(request):
    if request.method == 'POST':
        form = SchoolInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'School info added successfully!')
            return redirect('main:school_info_list')
    else:
        form = SchoolInfoForm()
    return render(request, 'main/custom_admin/school_info_form.html', {'form': form})

@superuser_required
def school_info_edit(request, info_id):
    info = get_object_or_404(SchoolInfo, id=info_id)
    if request.method == 'POST':
        form = SchoolInfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'School info updated successfully!')
            return redirect('main:school_info_list')
    else:
        form = SchoolInfoForm(instance=info)
    return render(request, 'main/custom_admin/school_info_form.html', {'form': form, 'info': info})

@superuser_required
def school_info_delete(request, info_id):
    info = get_object_or_404(SchoolInfo, id=info_id)
    if request.method == 'POST':
        info.delete()
        messages.success(request, 'School info deleted successfully!')
        return redirect('main:school_info_list')
    return render(request, 'main/custom_admin/school_info_confirm_delete.html', {'info': info})


# Contact Info Management
@superuser_required
def contact_info_list(request):
    infos = ContactInfo.objects.all().order_by('-is_active', '-updated_date')
    return render(request, 'main/custom_admin/contact_info_list.html', {'infos': infos})

@superuser_required
def contact_info_add(request):
    if request.method == 'POST':
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact info added successfully!')
            return redirect('main:contact_info_list')
    else:
        form = ContactInfoForm()
    return render(request, 'main/custom_admin/contact_info_form.html', {'form': form})

@superuser_required
def contact_info_edit(request, info_id):
    info = get_object_or_404(ContactInfo, id=info_id)
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact info updated successfully!')
            return redirect('main:contact_info_list')
    else:
        form = ContactInfoForm(instance=info)
    return render(request, 'main/custom_admin/contact_info_form.html', {'form': form, 'info': info})

@superuser_required
def contact_info_delete(request, info_id):
    info = get_object_or_404(ContactInfo, id=info_id)
    if request.method == 'POST':
        info.delete()
        messages.success(request, 'Contact info deleted successfully!')
        return redirect('main:contact_info_list')
    return render(request, 'main/custom_admin/contact_info_confirm_delete.html', {'info': info})


# Exam Type Management
@superuser_required
def exam_type_list(request):
    types = ExamType.objects.all().order_by('order', 'name')
    return render(request, 'main/custom_admin/exam_type_list.html', {'types': types})

@superuser_required
def exam_type_add(request):
    if request.method == 'POST':
        form = ExamTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam type added successfully!')
            return redirect('main:exam_type_list')
    else:
        form = ExamTypeForm()
    return render(request, 'main/custom_admin/exam_type_form.html', {'form': form})

@superuser_required
def exam_type_edit(request, type_id):
    type_obj = get_object_or_404(ExamType, id=type_id)
    if request.method == 'POST':
        form = ExamTypeForm(request.POST, instance=type_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam type updated successfully!')
            return redirect('main:exam_type_list')
    else:
        form = ExamTypeForm(instance=type_obj)
    return render(request, 'main/custom_admin/exam_type_form.html', {'form': form, 'type_obj': type_obj})

@superuser_required
def exam_type_delete(request, type_id):
    type_obj = get_object_or_404(ExamType, id=type_id)
    if request.method == 'POST':
        type_obj.delete()
        messages.success(request, 'Exam type deleted successfully!')
        return redirect('main:exam_type_list')
    return render(request, 'main/custom_admin/exam_type_confirm_delete.html', {'type_obj': type_obj})


# Student Class Management
@superuser_required
def student_class_list(request):
    classes = StudentClass.objects.all().order_by('order', 'name')
    return render(request, 'main/custom_admin/student_class_list.html', {'classes': classes})

@superuser_required
def student_class_add(request):
    if request.method == 'POST':
        form = StudentClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student class added successfully!')
            return redirect('main:student_class_list')
    else:
        form = StudentClassForm()
    return render(request, 'main/custom_admin/student_class_form.html', {'form': form})

@superuser_required
def student_class_edit(request, class_id):
    class_obj = get_object_or_404(StudentClass, id=class_id)
    if request.method == 'POST':
        form = StudentClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student class updated successfully!')
            return redirect('main:student_class_list')
    else:
        form = StudentClassForm(instance=class_obj)
    return render(request, 'main/custom_admin/student_class_form.html', {'form': form, 'class_obj': class_obj})

@superuser_required
def student_class_delete(request, class_id):
    class_obj = get_object_or_404(StudentClass, id=class_id)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Student class deleted successfully!')
        return redirect('main:student_class_list')
    return render(request, 'main/custom_admin/student_class_confirm_delete.html', {'class_obj': class_obj})


# Classwise Student Count Management
@superuser_required
def student_count_list(request):
    counts = ClasswiseStudentCount.objects.all().order_by('academic_year', 'student_class__order')
    return render(request, 'main/custom_admin/student_count_list.html', {'counts': counts})

@superuser_required
def student_count_add(request):
    if request.method == 'POST':
        form = ClasswiseStudentCountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student count added successfully!')
            return redirect('main:student_count_list')
    else:
        form = ClasswiseStudentCountForm()
    return render(request, 'main/custom_admin/student_count_form.html', {'form': form})

@superuser_required
def student_count_edit(request, count_id):
    count = get_object_or_404(ClasswiseStudentCount, id=count_id)
    if request.method == 'POST':
        form = ClasswiseStudentCountForm(request.POST, instance=count)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student count updated successfully!')
            return redirect('main:student_count_list')
    else:
        form = ClasswiseStudentCountForm(instance=count)
    return render(request, 'main/custom_admin/student_count_form.html', {'form': form, 'count': count})

@superuser_required
def student_count_delete(request, count_id):
    count = get_object_or_404(ClasswiseStudentCount, id=count_id)
    if request.method == 'POST':
        count.delete()
        messages.success(request, 'Student count deleted successfully!')
        return redirect('main:student_count_list')
    return render(request, 'main/custom_admin/student_count_confirm_delete.html', {'count': count})
