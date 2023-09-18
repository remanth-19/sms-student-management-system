from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


admin.site.register(Library)
admin.site.register(Books)
admin.site.register(BookIssue)
