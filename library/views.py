import json
import math
import datetime
from django.db.models import Sum
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from school_admin.forms import *

def library_home(request):
    total_books = Books.objects.all().count()
    total_categories = Category.objects.all().count()
    book = Books.objects.all()
    total_copies = Books.objects.aggregate(copies=Sum('no_of_copies'))
    context = {
        'page_title': "Library Dashboard",
        'total_books': total_books,
        'total_categories': total_categories,
        'total_copies': total_copies["copies"]

    }
    return render(request, '../../library/templates/home_content.html', context)

def add_book(request):
    form = BookForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'SMS | Add a New Book'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            author = form.cleaned_data.get('author')
            category = form.cleaned_data.get('category')
            no_of_copies = form.cleaned_data.get('no_of_copies')
            try:
                book = Books()
                book.name = name
                book.author = author
                book.category = category
                book.no_of_copies = no_of_copies
                book.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_book'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, '../../library/templates/add_book.html', context)

def add_book_category(request):
    form = CategoryForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'SMS | Add Book category'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                category = Category()
                category.name = name
                category.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_book_category'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, '../../library/templates/add_book_category.html', context)

def book_issue(request):
    category = Category.objects.all()
    students = CustomUser.objects.filter(user_type=3)
    context = {
        'categories': category,
        'students': students,
        'page_title': 'SMS | Issue Books to student'
    }

    return render(request, '../../library/templates/issue_book.html', context)

def manage_books(request):
    books = Books.objects.all()
    context = {
        'books': books,
        'page_title': 'SMS | Manage Books'
    }
    return render(request, "../../library/templates/manage_books.html", context)

def edit_book(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    form = BookForm(request.POST or None, instance=book)
    context = {
        'form': form,
        'faculty_id': book_id,
        'page_title': 'SMS | Edit Book Details'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_book', args=[book_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fill form properly")
    else:
        book = Books.objects.get(id=book_id)
        return render(request, "../../library/templates/edit_book.html", context)
    
def delete_book(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    try:
        book.delete()
        messages.success(request, "Book deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some students have borrowed this book already. Kindly collect the books from students and try again")
    return redirect(reverse('manage_books'))

@csrf_exempt
def get_books(request):
    category_id = request.POST.get('category')
    try:
        category = get_object_or_404(Category, id=category_id)
        books = Books.objects.filter(category=category)
        books_data = []
        for book in books:
            data = {
                    "id": book.id,
                    "name": book.name
                    }
            books_data.append(data)
        return JsonResponse(json.dumps(books_data), content_type='application/json', safe=False)
    except Exception as e:
        return e
    
@csrf_exempt
def save_book_issue_data(request):
    book_id = request.POST.get('book')
    date = request.POST.get('date')
    student_id = request.POST.get('student')
    category_id = request.POST.get('category')
    
    category = get_object_or_404(Category, id=category_id)
    student = get_object_or_404(Student, admin_id=student_id)
    book = get_object_or_404(Books, id=book_id)
    try:

        book_issue,created = BookIssue.objects.get_or_create(student=student, book=book, category=category, issue_date=date)
        if created:
            book_issue.save()

    except Exception as e:
        return None

    return HttpResponse("OK")

@csrf_exempt
def view_issued_books(request):
    if request.method != 'POST':
        issued_books = BookIssue.objects.all()
        context = {
            'issued_books': issued_books,
            'page_title': 'SMS | List of Issued Books'
        }
        return render(request, "view_issued_books.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        try:
            issue_book = get_object_or_404(BookIssue, id=id)
            issue_book.status = status
            issue_book.save()
            return HttpResponse(True)
        except Exception as e:
            return False


