# Generated by Django 5.2.1 on 2025-06-07 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0002_student_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
    ]
