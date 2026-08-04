from django.urls import path

from .views import (
    BookCreateView,
    BookDeleteView,
    BookDetailView,
    BookListView,
    BookUpdateView,
    CompletionReviewUpdateView,
    DashboardView,
    ReadingNoteCreateView,
    ReadingNoteDeleteView,
    ReadingNoteUpdateView,
)


urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("books/add/", BookCreateView.as_view(), name="book-add"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book-edit"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path(
        "books/<int:pk>/review/",
        CompletionReviewUpdateView.as_view(),
        name="book-review",
    ),
    path(
        "books/<int:book_pk>/notes/add/",
        ReadingNoteCreateView.as_view(),
        name="note-add",
    ),
    path(
        "notes/<int:pk>/edit/",
        ReadingNoteUpdateView.as_view(),
        name="note-edit",
    ),
    path(
        "notes/<int:pk>/delete/",
        ReadingNoteDeleteView.as_view(),
        name="note-delete",
    ),
]
