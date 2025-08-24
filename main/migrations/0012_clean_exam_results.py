from django.db import migrations

def clean_exam_results(apps, schema_editor):
    ExamResult = apps.get_model('main', 'ExamResult')
    # Delete any exam results with null values as they would be invalid
    ExamResult.objects.filter(student_class__isnull=True).delete()
    ExamResult.objects.filter(exam_type__isnull=True).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0011_classwisestudentcount'),
    ]

    operations = [
        migrations.RunPython(clean_exam_results, migrations.RunPython.noop),
    ]
