# Generated by Django 5.2.4 on 2025-07-15 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Headmaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='headmaster/')),
                ('qualification', models.CharField(blank=True, max_length=200)),
                ('experience_years', models.PositiveIntegerField(default=0, help_text='Years of experience')),
                ('contact_info', models.CharField(blank=True, max_length=200)),
                ('bio', models.TextField(help_text='About the headmaster')),
                ('message', models.TextField(blank=True, help_text='Message from headmaster to students/parents')),
                ('achievements', models.TextField(blank=True, help_text='Key achievements and awards')),
                ('education', models.TextField(blank=True, help_text='Educational background')),
                ('is_active', models.BooleanField(default=True, help_text='Is currently serving as headmaster')),
            ],
            options={
                'ordering': ['-is_active', 'name'],
            },
        ),
    ]
