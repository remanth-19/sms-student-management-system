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
    path("", views.login_page, name='login_page'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("admin/home/", views.admin_home, name='admin_home'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("student/manage/", views.manage_student, name='manage_student'),
    path("faculty/manage/", views.manage_faculty, name='manage_faculty'),
    path("session/manage/",views.manage_session, name='manage_session'),
    path("subject/manage/",views.manage_subject, name='manage_subject'),
    path("department/manage/", views.manage_department, name='manage_department'),
    path("add_session/", views.add_session, name='add_session'),
    path("student/manage/", views.manage_student, name='manage_student'),
    path("student/add/", views.add_student, name='add_student'),
    path("faculty/add", views.add_faculty, name='add_faculty'),
    path("department/add", views.add_department, name='add_department'),
    path("subject/add/", views.add_subject, name='add_subject'),
    path("faculty/edit/<int:staff_id>", views.edit_faculty, name='edit_faculty'),
    path("faculty/delete/<int:staff_id>",views.delete_faculty, name='delete_faculty'),
    path("department/delete/<int:department_id>",views.delete_department, name='delete_department'),
    path("subject/delete/<int:subject_id>",views.delete_subject, name='delete_subject'),
    path("session/delete/<int:session_id>",views.delete_session, name='delete_session'),
    path("student/delete/<int:student_id>",views.delete_student, name='delete_student'),
    path("student/edit/<int:student_id>",views.edit_student, name='edit_student'),
    path("department/edit/<int:department_id>",views.edit_department, name='edit_department'),
    path("subject/edit/<int:subject_id>",views.edit_subject, name='edit_subject'),
    path("session/edit/<int:session_id>",views.edit_session, name='edit_session'),
    path("admin/view_profile", views.admin_view_profile,name='admin_view_profile'),
    path("check_email_availability", views.check_email_availability,name="check_email_availability"),
    path("send_student_notification/", views.send_student_notification,name='send_student_notification'),
    path("send_faculty_notification/", views.send_faculty_notification,name='send_faculty_notification'),
    path("admin_notify_student", views.admin_notify_student,name='admin_notify_student'),
    path("admin_notify_faculty", views.admin_notify_faculty,name='admin_notify_faculty'),
    path("student/view/feedback/", views.student_feedback_message,name="student_feedback_message",),
    path("faculty/view/feedback/", views.faculty_feedback_message,name="faculty_feedback_message",),
    path("student/view/leave/", views.view_student_leave,name="view_student_leave",),
    path("staff/view/leave/", views.view_faculty_leave, name="view_faculty_leave",),
    path("attendance/view/", views.admin_view_attendance,name="admin_view_attendance",),
    path("attendance/fetch/", views.get_admin_attendance,name='get_admin_attendance'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("library/add/admin", views.add_library_admin, name='add_library_admin'),
    path("library/edit/admin/<int:library_id>", views.edit_library_admin, name='edit_library_admin'),
    path("library/manage/admin", views.manage_library_admin, name='manage_library_admin'),
    path("library/delete/admin/<int:library_id>",views.delete_library_admin, name='delete_library_admin'),
]