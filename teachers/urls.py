"""school_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

#from main_app.EditResultView import EditResultView

from . import views

urlpatterns = [
    path("home/", views.faculty_home, name='faculty_home'),
    path("fcmtoken/", views.faculty_fcmtoken, name='faculty_fcmtoken'),
    path("faculty/view/profile/", views.faculty_view_profile,name='faculty_view_profile'),
    path("faculty/apply/leave/", views.faculty_apply_leave,name='faculty_apply_leave'),
    path("faculty/feedback/", views.faculty_feedback, name='faculty_feedback'),
    path("faculty/view/profile/", views.faculty_view_profile, name='faculty_view_profile'),
    path("faculty/attendance/take/", views.faculty_take_attendance, name='faculty_take_attendance'),
    path("faculty/attendance/update/", views.faculty_update_attendance, name='faculty_update_attendance'),
    path("faculty/get_students/", views.get_students, name='get_students'),
    path("faculty/attendance/fetch/", views.get_student_attendance, name='get_student_attendance'),
    path("faculty/attendance/save/", views.save_attendance, name='save_attendance'),
    path("faculty/attendance/update/",views.update_attendance, name='update_attendance'),
    path("faculty/view/notification/", views.faculty_view_notification,name="faculty_view_notification"),
    path("faculty/add/assignment/", views.add_assignment,name="add_assignment"),
    path("faculty/result/add/", views.faculty_add_result, name='faculty_add_result'),
    #path("faculty/result/edit/", EditResultView.as_view(),name='edit_student_result'),
    path('faculty/result/fetch/', views.fetch_student_result,name='fetch_student_result'),
]