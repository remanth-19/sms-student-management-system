from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *
from student.models import Student, NotificationStudent, FeedbackStudent, LeaveReportStudent, StudentResult, AssignmentSubmission
from teachers.models import Faculty, Subject, NotificationFaculty, FeedbackFaculty, LeaveReportFaculty, Attendance, AttendanceReport, Assignment
from library.models import Library, Books, Category

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password' ]


class FacultyForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Faculty
        fields = CustomUserForm.Meta.fields + \
            ['department' ]

class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + \
            ['department', 'session']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields

class LibAdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(LibAdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Library
        fields = CustomUserForm.Meta.fields

class DepartmentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Department

class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name', 'faculty', 'department']

class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }

class FacultyEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(FacultyEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Faculty
        fields = CustomUserForm.Meta.fields

class LeaveReportFacultyForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportFacultyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportFaculty
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackFacultyForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackFacultyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackFaculty
        fields = ['feedback']

class FeedbackStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(FeedbackStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStudent
        fields = ['feedback']


class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields 

class LeaveReportStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStudent
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

class BookForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Books
        fields = ['name', 'author', 'no_of_copies', 'category']

class CategoryForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Category

class AssignmentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
    
    class Meta:
        fields = ['name','faculty','subject','session','assignment_pdf']
        model = Assignment

class SubmitAssignmentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SubmitAssignmentForm, self).__init__(*args, **kwargs)
    
    class Meta:
        fields = ['student','assignment','submit_assignment_pdf']
        model = AssignmentSubmission