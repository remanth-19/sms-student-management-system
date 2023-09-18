from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from school_admin.models import CustomUser
from student.models import Student


class Library(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name
    
class Category(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Books(models.Model):
    name = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    no_of_copies = models.IntegerField(default=1)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
    
class BookIssue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Books, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,default='')
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=200)
    status = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.book.name + "issued to" + self.student.last_name + " " + self.student.first_name
    
class BookBorrow(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Books, on_delete=models.DO_NOTHING)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=200)

    def __str__(self):
        return self.student.last_name + " " + self.student.first_name + "borrowed" + self.book.name
    
