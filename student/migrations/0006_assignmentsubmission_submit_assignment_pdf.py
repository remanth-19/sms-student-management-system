# Generated by Django 4.2.5 on 2023-09-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_assignmentsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='submit_assignment_pdf',
            field=models.FileField(default='', upload_to='submission_pdfs/'),
        ),
    ]
