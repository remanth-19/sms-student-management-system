# Generated by Django 4.2.5 on 2023-09-17 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_bookissue_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissue',
            name='due_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='issue_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='return_date',
            field=models.DateTimeField(),
        ),
    ]
