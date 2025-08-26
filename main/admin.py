from django.contrib import admin
from .models import (Notice, Teacher, OtherEmployee, CommitteeMember, Headmaster, SchoolInfo,
                     GalleryCategory, GalleryImage, NavigationLink, ContactInfo,
                     ExamResult, HomepageSlider, ExamType, StudentClass, ClasswiseStudentCount)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'notice_type', 'is_important', 'upload_date', 'created_by']
    list_filter = ['notice_type', 'is_important', 'upload_date', 'created_by']
    search_fields = ['title', 'content', 'summary']
    readonly_fields = ['upload_date']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'notice_type', 'is_important')
        }),
        ('PDF Notice', {
            'fields': ('pdf_file',),
            'description': 'Upload PDF file (only for PDF type notices)',
            'classes': ('collapse',)
        }),
        ('Text Notice', {
            'fields': ('summary', 'content'),
            'description': 'Write notice content (only for text type notices)',
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('upload_date',),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ('admin/js/notice_admin.js',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'subject', 'contact_info']
    list_filter = ['designation', 'subject']
    search_fields = ['name', 'subject', 'designation']
    fields = ['name', 'designation', 'subject', 'photo', 'contact_info', 'bio']


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order', 'contact_info']
    list_filter = ['role']
    search_fields = ['name', 'role']
    fields = ['name', 'role', 'photo', 'contact_info', 'order']
    list_editable = ['order']


@admin.register(Headmaster)
class HeadmasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'qualification', 'experience_years', 'is_active']
    list_filter = ['is_active', 'experience_years']
    search_fields = ['name', 'qualification']
    fields = ['name', 'photo', 'qualification', 'experience_years', 'contact_info',
              'bio', 'message', 'achievements', 'education', 'is_active']
    list_editable = ['is_active']


@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline', 'established_year', 'is_active']
    list_filter = ['is_active', 'established_year']
    search_fields = ['name', 'tagline']
    fields = ['name', 'tagline', 'logo', 'established_year', 'address', 'phone',
              'email', 'website', 'about', 'is_active']
    list_editable = ['is_active']

    def has_add_permission(self, request):
        # Allow adding only if no active school info exists
        return not SchoolInfo.objects.filter(is_active=True).exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting the active school info
        if obj and obj.is_active:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'image_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    fields = ['name', 'description', 'order', 'is_active']

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'order', 'upload_date', 'uploaded_by']
    list_filter = ['category', 'is_featured', 'upload_date', 'uploaded_by']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'order']
    fields = ['title', 'image', 'category', 'description', 'is_featured', 'order']
    readonly_fields = ['upload_date', 'uploaded_by']

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ['upload_date', 'uploaded_by']
        return self.readonly_fields


@admin.register(NavigationLink)
class NavigationLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'link_type', 'order', 'is_active', 'created_date'
                    ]
    list_filter = ['position', 'link_type', 'is_active', 'created_date']
    search_fields = ['title', 'title_bn', 'description']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'title_bn', 'position', 'order', 'is_active')
        }),
        ('Link Configuration', {
            'fields': ('link_type', 'url', 'internal_page', 'file_upload', 'open_new_tab')
        }),
        ('Display Options', {
            'fields': ('icon_class', 'description'),
            'classes': ('collapse',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Add help text for internal_page field
        if 'internal_page' in form.base_fields:
            form.base_fields['internal_page'].help_text = """
            Common internal pages:
            • main:home - Homepage
            • main:notices - Notices page
            • main:teachers - Teachers page
            • main:headmaster - Headmaster page
            • main:gallery - Gallery page
            • main:committee - Committee page
            • main:contact - Contact page
            """

        return form


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['page_title', 'general_email', 'main_phone', 'is_active', 'updated_date']
    list_filter = ['is_active', 'created_date', 'updated_date']
    search_fields = ['page_title', 'address', 'general_email', 'main_phone']
    list_editable = ['is_active']

    fieldsets = (
        ('Page Information', {
            'fields': ('page_title', 'page_title_bn', 'page_subtitle', 'page_subtitle_bn')
        }),
        ('Address', {
            'fields': ('address', 'address_bn')
        }),
        ('Phone Numbers', {
            'fields': ('main_phone', 'admissions_phone', 'additional_phone')
        }),
        ('Email Addresses', {
            'fields': ('general_email', 'admissions_email')
        }),
        ('Office Hours', {
            'fields': ('office_hours', 'office_hours_bn')
        }),
        ('Map Information', {
            'fields': ('map_embed_code', 'latitude', 'longitude'),
            'classes': ('collapse',),
            'description': 'Add Google Maps embed code or coordinates for location display'
        }),
        ('Contact Form', {
            'fields': ('enable_contact_form', 'form_title', 'form_title_bn')
        }),
        ('Additional Information', {
            'fields': ('additional_info', 'additional_info_bn'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        })
    )

    def has_add_permission(self, request):
        # Allow adding only if no active contact info exists
        return not ContactInfo.objects.filter(is_active=True).exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting the active contact info
        if obj and obj.is_active:
            return False
        return super().has_delete_permission(request, obj)






@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['title', 'student_class', 'exam_type', 'result_publish_date', 'is_published', 'uploaded_by']
    list_filter = ['student_class', 'exam_type', 'is_published', 'result_publish_date', 'uploaded_by']
    search_fields = ['title', 'description']
    list_editable = ['is_published']
    date_hierarchy = 'result_publish_date'
    readonly_fields = ['upload_date', 'updated_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'student_class', 'exam_type', 'result_type')
        }),
        ('File Upload', {
            'fields': ('result_file',),
            'description': 'Upload PDF or image file containing the exam results'
        }),
        ('Exam Details', {
            'fields': ('exam_date', 'result_publish_date', 'description')
        }),
        ('Publication Settings', {
            'fields': ('is_published',)
        }),
        ('Metadata', {
            'fields': ('upload_date', 'updated_date'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ['uploaded_by']
        return self.readonly_fields
    
    actions = ['publish_results', 'unpublish_results']
    
    def publish_results(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} results published.")
    publish_results.short_description = "Publish selected results"
    
    def unpublish_results(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} results unpublished.")
    unpublish_results.short_description = "Unpublish selected results"


@admin.register(HomepageSlider)
class HomepageSliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'is_active', 'created_date', 'created_by']
    list_filter = ['is_active', 'created_by']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_date']
    
    fieldsets = (
        ('Slide Content', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ['created_by']
        return self.readonly_fields
    
    actions = ['activate_slides', 'deactivate_slides']
    
    def activate_slides(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} slides activated.")
    activate_slides.short_description = "Activate selected slides"
    
    def deactivate_slides(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} slides deactivated.")
    deactivate_slides.short_description = "Deactivate selected slides"


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']


@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']


@admin.register(ClasswiseStudentCount)
class ClasswiseStudentCountAdmin(admin.ModelAdmin):
    list_display = ['student_class', 'academic_year', 'total_students',
                    'total_male', 'total_female', 'last_updated']
    list_filter = ['academic_year', 'student_class']
    search_fields = ['student_class__name', 'academic_year']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student_class', 'academic_year')
        }),
        ('Student Counts', {
            'fields': ('total_students', 'total_male', 'total_female')
        })
    )
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return ['student_class', 'academic_year']
        return []


@admin.register(OtherEmployee)
class OtherEmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'contact_info']
    list_filter = ['designation']
    search_fields = ['name', 'designation', 'contact_info']
    fields = ['name', 'designation', 'photo', 'contact_info', 'bio']
