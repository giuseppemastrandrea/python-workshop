from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Book, Author
from .forms import BookForm


class SecureBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    login_url = "/login/"  # Reindirizza alla pagina di login


class SecureBookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("book-list")


class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"


class AuthorListView(ListView):
    model = Author
    template_name = "books/author_list.html"
    context_object_name = "authors"


class AuthorDetailView(DetailView):
    model = Author
    template_name = "books/author_detail.html"
    context_object_name = "author"
