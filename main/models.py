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


class ContactInfo(models.Model):
    # Basic Information
    page_title = models.CharField(max_length=200, default="Contact Us")
    page_title_bn = models.CharField(max_length=200, blank=True, help_text="Bengali page title")
    page_subtitle = models.CharField(max_length=300, default="Get in touch with us for any inquiries or information")
    page_subtitle_bn = models.CharField(max_length=300, blank=True, help_text="Bengali page subtitle")

    # Address Information
    address = models.TextField(help_text="Full address of the school")
    address_bn = models.TextField(blank=True, help_text="Bengali address")

    # Phone Numbers
    main_phone = models.CharField(max_length=50, help_text="Main office phone number")
    admissions_phone = models.CharField(max_length=50, blank=True, help_text="Admissions phone number")
    additional_phone = models.CharField(max_length=50, blank=True, help_text="Additional phone number")

    # Email Addresses
    general_email = models.EmailField(help_text="General contact email")
    admissions_email = models.EmailField(blank=True, help_text="Admissions email")

    # Office Hours
    office_hours = models.TextField(help_text="Office hours information")
    office_hours_bn = models.TextField(blank=True, help_text="Bengali office hours")

    # Map Information
    map_embed_code = models.TextField(blank=True, help_text="Google Maps embed code (iframe)")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True, help_text="Latitude for map")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True, help_text="Longitude for map")

    # Contact Form Settings
    enable_contact_form = models.BooleanField(default=True, help_text="Enable contact form on the page")
    form_title = models.CharField(max_length=200, default="Send us a Message")
    form_title_bn = models.CharField(max_length=200, blank=True, help_text="Bengali form title")

    # Additional Information
    additional_info = models.TextField(blank=True, help_text="Any additional contact information")
    additional_info_bn = models.TextField(blank=True, help_text="Bengali additional information")

    # Meta
    is_active = models.BooleanField(default=True, help_text="Use this contact information")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
        ordering = ['-is_active', '-updated_date']

    def __str__(self):
        return f"Contact Info - {self.page_title}"

    def save(self, *args, **kwargs):
        # Ensure only one active contact info exists
        if self.is_active:
            ContactInfo.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class ExamType(models.Model):
    name = models.CharField(max_length=50, help_text="Name of the exam type (e.g., 'First Term')")
    code = models.CharField(max_length=20, unique=True, help_text="Short code for the exam type (e.g., 'first_term')")
    description = models.TextField(blank=True, help_text="Description of this exam type")
    order = models.PositiveIntegerField(default=0, help_text="Display order in lists")
    is_active = models.BooleanField(default=True, help_text="Whether this exam type is currently in use")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Exam Type"
        verbose_name_plural = "Exam Types"

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=50, help_text="Class name (e.g., 'Class 6')")
    code = models.CharField(max_length=10, unique=True, help_text="Short code for the class (e.g., '6')")
    description = models.TextField(blank=True, help_text="Description of this class")
    order = models.PositiveIntegerField(default=0, help_text="Display order in lists")
    is_active = models.BooleanField(default=True, help_text="Whether this class is currently accepting students")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Student Class"
        verbose_name_plural = "Student Classes"

    def __str__(self):
        return self.name


class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
    ]
    
    SECTION_CHOICES = [
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C'),
    ]

    name = models.CharField(max_length=100, help_text="Student's full name")
    roll_number = models.CharField(max_length=20, help_text="Student roll number")
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES, help_text="Student's class")
    section = models.CharField(max_length=5, choices=SECTION_CHOICES, default='A', help_text="Student's section")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, help_text="Student's gender")
    admission_date = models.DateField(help_text="Date of admission")
    is_active = models.BooleanField(default=True, help_text="Is currently enrolled")

    class Meta:
        ordering = ['class_name', 'section', 'roll_number']
        unique_together = ['roll_number', 'class_name', 'section']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.name} - Class {self.class_name}{self.section} (Roll: {self.roll_number})"

    def get_full_class(self):
        """Return full class name with section"""
        return f"Class {self.class_name}{self.section}"


class ExamResult(models.Model):
    RESULT_TYPE_CHOICES = [
        ('pdf', 'PDF File'),
        ('image', 'Image File'),
        ('text', 'Text Content'),
    ]

    title = models.CharField(max_length=200, help_text="Result title (e.g., 'First Term Exam 2024')")
    student_class = models.ForeignKey(StudentClass, on_delete=models.PROTECT, 
                                    help_text="Class for this result", null=True)
    exam_type = models.ForeignKey(ExamType, on_delete=models.PROTECT,
                                 help_text="Type of examination", null=True)

    def save(self, *args, **kwargs):
        if not self.student_class or not self.exam_type:
            raise ValueError("Both student_class and exam_type are required")
    result_type = models.CharField(max_length=10, choices=RESULT_TYPE_CHOICES, default='pdf',
                                   help_text="Choose file type for result")
    
    # File uploads
    result_file = models.FileField(upload_to='exam_results/', blank=True, null=True,
                                   help_text="Upload PDF or image file")
    
    # Text content
    text_content = models.TextField(blank=True, null=True,
                                  help_text="Enter result content if using text format")
    
    # Additional information
    exam_date = models.DateField(help_text="Date when exam was conducted")
    result_publish_date = models.DateField(help_text="Date when result was published")
    description = models.TextField(blank=True, help_text="Additional information about the exam")
    
    # Meta information
    is_published = models.BooleanField(default=False, help_text="Make result visible to public")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-result_publish_date', 'student_class', 'exam_type']
        verbose_name = "Exam Result"
        verbose_name_plural = "Exam Results"

    def __str__(self):
        return f"{self.title} - {self.student_class} ({self.exam_type})"

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.result_type in ['pdf', 'image'] and not self.result_file:
            raise ValidationError("File upload is required for PDF and Image type results.")
        
        if self.result_type == 'text' and not self.text_content:
            raise ValidationError("Text content is required for Text type results.")
        
        if self.result_type == 'text' and self.result_file:
            raise ValidationError("File should not be uploaded for Text type results.")
        
        if self.result_type in ['pdf', 'image'] and self.text_content:
            raise ValidationError("Text content should be empty for PDF and Image type results.")

    def get_file_extension(self):
        """Get file extension for display purposes"""
        if self.result_file:
            return self.result_file.name.split('.')[-1].upper()
        return None


class HomepageSlider(models.Model):
    image = models.ImageField(upload_to='slider/', help_text="Slider image (recommended: 1920x800px)")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True, help_text="Show this slide")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Homepage Slider"
        verbose_name_plural = "Homepage Sliders"

    def __str__(self):
        return f"Slider Image {self.id} (Order: {self.order})"


class ClasswiseStudentCount(models.Model):
    student_class = models.ForeignKey(StudentClass, on_delete=models.PROTECT,
                                    help_text="Class for which to record student count")
    academic_year = models.PositiveIntegerField(help_text="Academic year (e.g., 2025)")
    total_students = models.PositiveIntegerField(help_text="Total number of students in this class")
    total_male = models.PositiveIntegerField(help_text="Number of male students", default=0)
    total_female = models.PositiveIntegerField(help_text="Number of female students", default=0)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['academic_year', 'student_class__order']
        unique_together = ['student_class', 'academic_year']
        verbose_name = "Class-wise Student Count"
        verbose_name_plural = "Class-wise Student Counts"

    def __str__(self):
        return f"{self.student_class.name} - {self.academic_year} ({self.total_students} students)"

    def clean(self):
        from django.core.exceptions import ValidationError

        # Validate that male + female equals total
        if self.total_male + self.total_female != self.total_students:
            raise ValidationError("Sum of male and female students must equal total students")
