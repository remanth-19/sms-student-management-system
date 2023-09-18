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
    path("library/home/", views.library_home, name='library_home'),
    path("library/add/book", views.add_book, name='add_book'),
    path("library/add/category", views.add_book_category, name='add_book_category'),
    path("library/manage/books", views.manage_books, name='manage_books'),
    path("library/manage/category", views.library_home, name='manage_category'),
    path("library/edit/book/<int:book_id>", views.edit_book, name='edit_book'),
    path("library/delete/book/<int:book_id>", views.delete_book, name='delete_book'),
    path("library/book/issue", views.book_issue, name='book_issue'),
    path("library/manage/copies", views.library_home, name='manage_copies'),
    path("library/get_books/", views.get_books, name='get_books'),
    path("library/book/issue/save", views.save_book_issue_data, name='save_book_issue_data'),
    path("library/view/books/issued", views.view_issued_books, name='view_issued_books'),

]