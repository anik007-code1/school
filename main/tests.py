from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import ExamResult, StudentClass, ExamType, OtherEmployee
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime


class ExamResultModelTests(TestCase):
    def setUp(self):
        # Create a user for uploaded_by
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

        # Create a student class
        self.student_class = StudentClass.objects.create(
            name='Class 6',
            code='6',
            description='Sixth grade',
            order=1,
            is_active=True
        )

        # Create an exam type
        self.exam_type = ExamType.objects.create(
            name='First Term',
            code='first_term',
            description='First term exams',
            order=1,
            is_active=True
        )

        # Simple PDF file for upload tests
        self.pdf_file = SimpleUploadedFile(
            "result.pdf",
            b"%PDF-1.4 test pdf content",
            content_type="application/pdf"
        )

    def test_exam_result_creation_success(self):
        """ExamResult should be saved correctly when all required fields are provided."""
        result = ExamResult.objects.create(
            title='First Term Exam 2024',
            student_class=self.student_class,
            exam_type=self.exam_type,
            result_type='pdf',
            result_file=self.pdf_file,
            exam_date=datetime.date(2024, 5, 20),
            result_publish_date=datetime.date(2024, 5, 25),
            uploaded_by=self.user
        )
        self.assertIsNotNone(result.id)
        self.assertFalse(result.is_published)  # default is False
        self.assertEqual(result.student_class, self.student_class)
        self.assertEqual(result.exam_type, self.exam_type)

    def test_exam_result_validation_file_missing_for_pdf(self):
        """Result with type 'pdf' but no file should fail validation."""
        result = ExamResult(
            title='No File PDF',
            student_class=self.student_class,
            exam_type=self.exam_type,
            result_type='pdf',
            exam_date=datetime.date.today(),
            result_publish_date=datetime.date.today(),
            uploaded_by=self.user
        )
        with self.assertRaises(ValidationError) as cm:
            result.full_clean()
        self.assertIn('File upload is required for PDF and Image type results.', str(cm.exception))

    def test_exam_result_publish_workflow(self):
        """ExamResult can be marked as published and retrieved via the published queryset."""
        result = ExamResult.objects.create(
            title='Publish Test',
            student_class=self.student_class,
            exam_type=self.exam_type,
            result_type='pdf',
            result_file=self.pdf_file,
            exam_date=datetime.date.today(),
            result_publish_date=datetime.date.today(),
            uploaded_by=self.user,
            is_published=True
        )
        published_qs = ExamResult.objects.filter(is_published=True)
        self.assertIn(result, published_qs)


class OtherEmployeeModelTests(TestCase):
    def test_other_employee_creation(self):
        """Test creating an OtherEmployee instance."""
        employee = OtherEmployee.objects.create(
            name='John Doe',
            designation='Cleaner',
            contact_info='0123456789'
        )
        self.assertEqual(str(employee), 'John Doe - Cleaner')
