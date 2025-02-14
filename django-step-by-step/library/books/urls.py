from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView,
    SecureBookCreateView,
)

from .views_api import (
    BookListCreate,
    BookRetrieveUpdateDestroy,
    AuthorListCreate,
    AuthorRetrieveUpdateDestroy,
)


urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("books/new/", SecureBookCreateView.as_view(), name="book-create"),
    path("api/books/", BookListCreate.as_view(), name="api-book-list"),
    path(
        "api/books/<int:pk>/",
        BookRetrieveUpdateDestroy.as_view(),
        name="api-book-detail",
    ),
    path("api/authors/", AuthorListCreate.as_view(), name="api-author-list"),
    path(
        "api/authors/<int:pk>/",
        AuthorRetrieveUpdateDestroy.as_view(),
        name="api-author-detail",
    ),
]
