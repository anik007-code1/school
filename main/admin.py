from django.contrib import admin
from .models import Notice, Teacher, CommitteeMember, Headmaster, SchoolInfo, GalleryCategory, GalleryImage


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
