from django import forms
from .models import (Notice, Teacher, OtherEmployee, CommitteeMember, Headmaster,
                     GalleryCategory, GalleryImage, ContactInfo, ExamResult, HomepageSlider,
                     ExamType, StudentClass, ClasswiseStudentCount, SchoolInfo)


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'notice_type', 'pdf_file', 'content', 'summary', 'is_important']
        widgets = {
            'notice_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter notice title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief summary'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'subject', 'designation', 'photo', 'contact_info', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject taught'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone/email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class OtherEmployeeForm(forms.ModelForm):
    class Meta:
        model = OtherEmployee
        fields = ['name', 'designation', 'photo', 'contact_info', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Role (e.g., Cleaner)'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone/email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class CommitteeMemberForm(forms.ModelForm):
    class Meta:
        model = CommitteeMember
        fields = ['name', 'role', 'photo', 'contact_info', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Role in committee'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone/email'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Display order'}),
        }


class HeadmasterForm(forms.ModelForm):
    class Meta:
        model = Headmaster
        fields = ['name', 'photo', 'qualification', 'experience_years', 'contact_info',
                 'bio', 'message', 'achievements', 'education', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qualifications'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone/email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['title', 'student_class', 'exam_type', 'result_type', 'result_file',
                 'text_content', 'exam_date', 'result_publish_date', 'description', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Result title'}),
            'student_class': forms.Select(attrs={'class': 'form-control'}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'result_type': forms.Select(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'result_publish_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'text_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HomepageSliderForm(forms.ModelForm):
    class Meta:
        model = HomepageSlider
        fields = ['image', 'order', 'is_active']
        widgets = {
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Display order'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GalleryCategoryForm(forms.ModelForm):
    class Meta:
        model = GalleryCategory
        fields = ['name', 'description', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'image', 'category', 'description', 'is_featured', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = '__all__'
        widgets = {
            'page_title': forms.TextInput(attrs={'class': 'form-control'}),
            'page_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'main_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'general_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'map_embed_code': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'enable_contact_form': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['name', 'code', 'description', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exam type name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StudentClassForm(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ['name', 'code', 'description', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ClasswiseStudentCountForm(forms.ModelForm):
    class Meta:
        model = ClasswiseStudentCount
        fields = ['student_class', 'academic_year', 'total_students', 'total_male', 'total_female']
        widgets = {
            'student_class': forms.Select(attrs={'class': 'form-control'}),
            'academic_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2025'}),
            'total_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_male': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_female': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = ['name', 'tagline', 'logo', 'address', 'phone', 'email', 'website', 'established_year', 'about', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School name'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School tagline'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact email'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'School website'}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }