# Generated by Django 4.2.5 on 2023-09-16 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_studentresult'),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('author', models.CharField(max_length=120)),
                ('no_of_copies', models.IntegerField(default=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.category')),
            ],
        ),
        migrations.CreateModel(
            name='BookIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(auto_now=True)),
                ('return_date', models.DateTimeField(auto_now=True)),
                ('remarks', models.CharField(max_length=200)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='library.books')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='BookBorrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(auto_now=True)),
                ('return_date', models.DateTimeField(auto_now=True)),
                ('remarks', models.CharField(max_length=200)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='library.books')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.student')),
            ],
        ),
    ]