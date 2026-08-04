from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import BookForm, ReadingNoteForm, RegistrationForm
from .models import Book, ReadingNote


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("book-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class OwnedBookQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self) -> QuerySet:
        return Book.objects.filter(owner=self.request.user)


class BookListView(OwnedBookQuerysetMixin, ListView):
    model = Book
    context_object_name = "books"
    template_name = "books/book_list.html"

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        if status in Book.ReadingStatus.values:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["selected_status"] = (
            status if status in Book.ReadingStatus.values else ""
        )
        context["status_choices"] = Book.ReadingStatus.choices
        context["filters_active"] = bool(
            context["search_query"] or context["selected_status"]
        )
        return context


class DashboardView(OwnedBookQuerysetMixin, ListView):
    model = Book
    context_object_name = "active_books"
    template_name = "books/dashboard.html"

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(
            status=Book.ReadingStatus.CURRENTLY_READING
        )


class BookDetailView(OwnedBookQuerysetMixin, DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BookUpdateView(OwnedBookQuerysetMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"


class BookDeleteView(OwnedBookQuerysetMixin, DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("book-list")


class ReadingNoteCreateView(LoginRequiredMixin, CreateView):
    model = ReadingNote
    form_class = ReadingNoteForm
    template_name = "books/note_form.html"

    def get_book(self) -> Book:
        if not hasattr(self, "book"):
            self.book = get_object_or_404(
                Book,
                pk=self.kwargs["book_pk"],
                owner=self.request.user,
            )
        return self.book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = self.get_book()
        return context

    def form_valid(self, form):
        form.instance.book = self.get_book()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.book.get_absolute_url()


class ReadingNoteUpdateView(LoginRequiredMixin, UpdateView):
    model = ReadingNote
    form_class = ReadingNoteForm
    template_name = "books/note_form.html"

    def get_queryset(self) -> QuerySet:
        return ReadingNote.objects.filter(book__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = self.object.book
        return context

    def get_success_url(self):
        return self.object.book.get_absolute_url()


class ReadingNoteDeleteView(LoginRequiredMixin, DeleteView):
    model = ReadingNote
    template_name = "books/note_confirm_delete.html"

    def get_queryset(self) -> QuerySet:
        return ReadingNote.objects.filter(book__owner=self.request.user)

    def get_success_url(self):
        return self.object.book.get_absolute_url()
