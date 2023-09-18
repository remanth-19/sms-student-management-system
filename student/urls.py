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



from . import views

urlpatterns = [
    path("student/home/", views.student_home, name='student_home'),
    path("student/view/attendance/", views.student_view_attendance,name='student_view_attendance'),
    path("student/view/assignments/", views.view_assignments,name='view_assignments'),
    path("student/apply/leave/", views.student_apply_leave,name='student_apply_leave'),
    path("student/feedback/", views.student_feedback, name='student_feedback'),
    path("student/view/profile/", views.student_view_profile, name='student_view_profile'),
    path("student/fcmtoken/", views.student_fcmtoken,name='student_fcmtoken'),
    path("student/view/notification/", views.student_view_notification,name="student_view_notification"),
    path("student/submit/assignment/<int:assignment_id>", views.student_submit_assignment,name="student_submit_assignment"),
    path('student/view/result/', views.student_view_result, name='student_view_result'),
    path('student/save/assignment/', views.save_assignment, name='save_assignment'),
    path("view/pdfs/<int:submission_id>",views.view_pdf,name='view_pdf'),
]