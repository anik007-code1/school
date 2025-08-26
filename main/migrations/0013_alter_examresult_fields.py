from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0012_clean_exam_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='student_class',
            field=models.ForeignKey(
                on_delete=models.PROTECT,
                to='main.StudentClass',
                help_text='Class for this result',
            ),
        ),
        migrations.AlterField(
            model_name='examresult',
            name='exam_type',
            field=models.ForeignKey(
                on_delete=models.PROTECT,
                to='main.ExamType',
                help_text='Type of examination',
            ),
        ),
    ]