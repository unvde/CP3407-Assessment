from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import BookForm, RegistrationForm
from .models import Book


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
