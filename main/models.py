from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Notice(models.Model):
    NOTICE_TYPE_CHOICES = [
        ('pdf', 'PDF Upload'),
        ('text', 'Text Content'),
    ]

    title = models.CharField(max_length=200)
    notice_type = models.CharField(max_length=10, choices=NOTICE_TYPE_CHOICES, default='pdf',
                                   help_text="Choose whether to upload a PDF or write text content")

    # For PDF notices
    pdf_file = models.FileField(upload_to='notices/', blank=True, null=True,
                                help_text="Upload PDF file (only for PDF type notices)")

    # For text notices
    content = models.TextField(blank=True,
                               help_text="Write notice content here (only for text type notices)")
    summary = models.CharField(max_length=300, blank=True,
                               help_text="Brief summary for text notices (optional)")

    upload_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_important = models.BooleanField(default=False, help_text="Mark as important notice")

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.title} ({self.get_notice_type_display()})"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.notice_type == 'pdf' and not self.pdf_file:
            raise ValidationError("PDF file is required for PDF type notices.")

        if self.notice_type == 'text' and not self.content:
            raise ValidationError("Content is required for text type notices.")

        if self.notice_type == 'pdf' and self.content:
            raise ValidationError("Content should be empty for PDF type notices.")

        if self.notice_type == 'text' and self.pdf_file:
            raise ValidationError("PDF file should not be uploaded for text type notices.")


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    contact_info = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.designation}"


class CommitteeMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='committee/', blank=True, null=True)
    contact_info = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.role}"


class Headmaster(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='headmaster/', blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0, help_text="Years of experience")
    contact_info = models.CharField(max_length=200, blank=True)
    bio = models.TextField(help_text="About the headmaster")
    message = models.TextField(blank=True, help_text="Message from headmaster to students/parents")
    achievements = models.TextField(blank=True, help_text="Key achievements and awards")
    education = models.TextField(blank=True, help_text="Educational background")
    is_active = models.BooleanField(default=True, help_text="Is currently serving as headmaster")

    class Meta:
        ordering = ['-is_active', 'name']

    def __str__(self):
        return f"{self.name} - Headmaster"


class SchoolInfo(models.Model):
    name = models.CharField(max_length=200, default="Noagaon High School")
    tagline = models.CharField(max_length=300, default="Excellence in Education Since 1950")
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, help_text="School logo")
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField(default=1950)
    about = models.TextField(blank=True, help_text="About the school")
    is_active = models.BooleanField(default=True, help_text="Use this school info")

    class Meta:
        verbose_name = "School Information"
        verbose_name_plural = "School Information"
        ordering = ['-is_active']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one active school info
            SchoolInfo.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Gallery Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False, help_text="Show in featured gallery")
    order = models.PositiveIntegerField(default=0, help_text="Order within category")

    class Meta:
        ordering = ['-is_featured', 'order', '-upload_date']

    def __str__(self):
        return f"{self.title} - {self.category.name}"


class NavigationLink(models.Model):
    LINK_TYPE_CHOICES = [
        ('internal', 'Internal Page'),
        ('external', 'External URL'),
        ('file', 'File Download'),
    ]

    POSITION_CHOICES = [
        ('main', 'Main Navigation'),
        ('important', 'Important Links'),
        ('footer', 'Footer Links'),
    ]

    title = models.CharField(max_length=100, help_text="Display name for the link")
    title_bn = models.CharField(max_length=100, blank=True, help_text="Bengali title (optional)")
    link_type = models.CharField(max_length=10, choices=LINK_TYPE_CHOICES, default='external')
    url = models.URLField(blank=True, help_text="External URL (for external links)")
    internal_page = models.CharField(max_length=100, blank=True,
                                   help_text="Internal page name (e.g., 'main:home', 'main:notices')")
    file_upload = models.FileField(upload_to='navigation_files/', blank=True, null=True,
                                 help_text="File to download (for file links)")
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='important')
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    open_new_tab = models.BooleanField(default=False, help_text="Open link in new tab")
    icon_class = models.CharField(max_length=100, blank=True,
                                help_text="CSS icon class (e.g., 'fas fa-home')")
    description = models.TextField(blank=True, help_text="Link description")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', 'order', 'title']
        verbose_name = "Navigation Link"
        verbose_name_plural = "Navigation Links"

    def __str__(self):
        return f"{self.title} ({self.get_position_display()})"

    def get_url(self):
        """Return the appropriate URL based on link type"""
        if self.link_type == 'external':
            return self.url
        elif self.link_type == 'internal' and self.internal_page:
            try:
                from django.urls import reverse
                return reverse(self.internal_page)
            except:
                return '#'
        elif self.link_type == 'file' and self.file_upload:
            return self.file_upload.url
        return '#'

    def get_title(self, language='en'):
        """Return title in specified language"""
        if language == 'bn' and self.title_bn:
            return self.title_bn
        return self.title
