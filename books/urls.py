from django.urls import path

from .views import (
    BookCreateView,
    BookDeleteView,
    BookDetailView,
    BookListView,
    BookUpdateView,
)


urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("books/add/", BookCreateView.as_view(), name="book-add"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book-edit"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
]

