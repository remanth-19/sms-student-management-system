import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .forms import *
from .models import *

from django.contrib.auth import authenticate, login, logout

from .EmailBackend import EmailBackend
#from .models import Attendance, Session, Subject

# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
        elif request.user.user_type == '3':
            return redirect(reverse("student_home"))
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        
        
        #Authenticate
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home"))
            elif user.user_type == '2':
                return redirect(reverse("staff_home"))
            elif user.user_type == '3':
                return redirect(reverse("student_home"))
            else:
                return redirect("/")
        else:
            messages.error(request, "Invalid details")
            return redirect("/")



def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")

def admin_home(request):
    total_faculty = Faculty.objects.all().count()
    total_students = Student.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    total_departments = Department.objects.all().count()
    #attendance_list = Attendance.objects.filter(subject__in=subjects)
    #total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    #for subject in subjects:
    #    attendance_count = Attendance.objects.filter(subject=subject).count()
    #    subject_list.append(subject.name[:7])
    #    attendance_list.append(attendance_count)
    context = {
        'page_title': "Administrative Dashboard",
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_department': total_departments,
        'total_subject': total_subject,
        #'subject_list': subject_list,
        #'attendance_list': attendance_list

    }
    return render(request, 'home_content.html', context)

def add_student(request):
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': 'School Management | Add Student'}
    if request.method == 'POST':
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            email = student_form.cleaned_data.get('email')
            gender = student_form.cleaned_data.get('gender')
            password = student_form.cleaned_data.get('password')
            department = student_form.cleaned_data.get('department')
            session = student_form.cleaned_data.get('session')
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name)
                user.gender = gender
                user.student.session = session
                user.student.department = department
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'add_student.html', context)

def add_faculty(request):
    form = FacultyForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'SMS | Add Faculty'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            department = form.cleaned_data.get('department')
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name)
                user.gender = gender
                user.faculty.department = department
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_faculty'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'add_faculty.html', context)

def add_department(request):
    form = DepartmentForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'SMS | Add Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                department = Department()
                department.name = name
                department.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_department'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'add_department.html', context)

def add_subject(request):
    form = SubjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'SMS | Add Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')
            faculty = form.cleaned_data.get('faculty')
            try:
                subject = Subject()
                subject.name = name
                subject.faculty = faculty
                subject.department = department
                subject.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_subject'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'add_subject.html', context)

def manage_student(request):
    students = CustomUser.objects.filter(user_type=3)
    context = {
        'students': students,
        'page_title': 'SMS | Manage Students'
    }
    return render(request, "manage_student.html", context)

def manage_faculty(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'SMS | Manage Faculty'
    }
    return render(request, "manage_faculty.html", context)

def manage_department(request):
    departments = Department.objects.all()
    context = {
        'departments': departments,
        'page_title': 'SMS | Manage Departments'
    }
    return render(request, "manage_department.html", context)

def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': 'SMS | Manage Subjects'
    }
    return render(request, "manage_subject.html", context)

def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'SMS | View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "admin_view_profile.html", context)

def edit_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    form = FacultyForm(request.POST or None, instance=faculty)
    context = {
        'form': form,
        'faculty_id': faculty_id,
        'page_title': 'SMS | Edit Faculty'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            department = form.cleaned_data.get('department')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=Faculty.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                faculty.department = department
                user.save()
                faculty.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_faculty', args=[faculty_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fill form properly")
    else:
        user = CustomUser.objects.get(id=faculty_id)
        faculty = Faculty.objects.get(id=user.id)
        return render(request, "edit_faculty.html", context)
    
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'form': form,
        'student_id': student_id,
        'page_title': 'SMS | Edit Student'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            department = form.cleaned_data.get('department')
            session = form.cleaned_data.get('session')
            try:
                user = CustomUser.objects.get(id=student.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                student.session = session
                user.gender = gender
                student.department = department
                user.save()
                student.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_student', args=[student_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "edit_student.html", context)


def edit_department(request, department_id):
    instance = get_object_or_404(Department, id=department_id)
    form = DepartmentForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'department_id': department_id,
        'page_title': 'SMS | Edit Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                department = Department.objects.get(id=department_id)
                department.name = name
                department.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'edit_department.html', context)


def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': 'SMS | Edit Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')
            faculty = form.cleaned_data.get('faculty')
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.name = name
                subject.faculty = faculty
                subject.department = department
                subject.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'edit_subject.html', context)

def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'SMS | Add Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "add_session.html", context)


def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'SMS | Manage Sessions'}
    return render(request, "manage_session.html", context)

def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': 'SMS | Edit Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "edit_session.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "edit_session.html", context)

    else:
        return render(request, "edit_session.html", context)


def delete_faculty(request, faculty_id):
    faculty = get_object_or_404(CustomUser, faculty__id=faculty_id)
    faculty.delete()
    messages.success(request, "Faculty member deleted successfully!")
    return redirect(reverse('manage_faculty'))

def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))


def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    try:
        department.delete()
        messages.success(request, "Department deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some students are aligned to this department already. Kindly change the affected student department and try again")
    return redirect(reverse('manage_department'))


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect(reverse('manage_subject'))


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are students assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))

@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)
    
def showFirebaseJS(request):
    data = """
    // Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
    apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
    authDomain: "sms-with-django.firebaseapp.com",
    databaseURL: "https://sms-with-django.firebaseio.com",
    projectId: "sms-with-django",
    storageBucket: "sms-with-django.appspot.com",
    messagingSenderId: "945324593139",
    appId: "1:945324593139:web:03fa99a8854bbd38420c86",
    measurementId: "G-2F2RXTL9GT"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {
    const notification = JSON.parse(payload);
    const notificationOption = {
        body: notification.body,
        icon: notification.icon
    }
    return self.registration.showNotification(payload.notification.title, notificationOption);
});
    """
    return HttpResponse(data, content_type='application/javascript')