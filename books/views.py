from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import signing
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Q, QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from .forms import (
    BookForm,
    CategoryForm,
    CompletionReviewForm,
    ForumForm,
    ForumPostForm,
    ForumReplyForm,
    ReadingNoteForm,
    RegistrationForm,
    parse_category_names,
)
from .models import (
    Book,
    CatalogBook,
    Category,
    Forum,
    ForumPost,
    ForumReply,
    ReadingNote,
)
from .services import BookSearchError, load_import_token, search_open_library


def get_or_create_category(name, user=None, source=Category.Source.USER):
    category = Category.objects.filter(name__iexact=name).first()
    if category:
        return category
    return Category.objects.create(name=name, created_by=user, source=source)


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
        category = self.request.GET.get("category", "").strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        if status in Book.ReadingStatus.values:
            queryset = queryset.filter(status=status)
        if category:
            queryset = queryset.filter(catalog_book__categories__slug=category)

        return queryset.select_related("catalog_book").prefetch_related(
            "catalog_book__categories"
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["selected_status"] = (
            status if status in Book.ReadingStatus.values else ""
        )
        context["status_choices"] = Book.ReadingStatus.choices
        context["categories"] = Category.objects.filter(
            books__shelf_entries__owner=self.request.user
        ).distinct()
        context["selected_category"] = self.request.GET.get("category", "").strip()
        context["filters_active"] = bool(
            context["search_query"]
            or context["selected_status"]
            or context["selected_category"]
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
        with transaction.atomic():
            catalog_book = CatalogBook.objects.create(
                title=form.cleaned_data["title"],
                author=form.cleaned_data["author"],
                added_by=self.request.user,
            )
            for name in form.cleaned_data.get("categories", []):
                catalog_book.categories.add(
                    get_or_create_category(name, self.request.user)
                )
            form.instance.owner = self.request.user
            form.instance.catalog_book = catalog_book
            return super().form_valid(form)


class BookUpdateView(OwnedBookQuerysetMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.catalog_book_id:
            for name in form.cleaned_data.get("categories", []):
                self.object.catalog_book.categories.add(
                    get_or_create_category(name, self.request.user)
                )
        return response


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


class CompletionReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = CompletionReviewForm
    context_object_name = "book"
    template_name = "books/review_form.html"

    def get_queryset(self) -> QuerySet:
        return Book.objects.filter(
            owner=self.request.user,
            status=Book.ReadingStatus.COMPLETED,
        )

    def get_success_url(self):
        return self.object.get_absolute_url()


class CatalogBookListView(ListView):
    model = CatalogBook
    context_object_name = "catalog_books"
    template_name = "books/catalog_list.html"
    paginate_by = 24

    def get_queryset(self):
        queryset = CatalogBook.objects.prefetch_related("categories")
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(author__icontains=query)
                | Q(isbn_10__icontains=query)
                | Q(isbn_13__icontains=query)
            )
        if category:
            queryset = queryset.filter(categories__slug=category)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["selected_category"] = self.request.GET.get("category", "").strip()
        context["categories"] = Category.objects.all()
        return context


class CatalogBookDetailView(DetailView):
    model = CatalogBook
    context_object_name = "catalog_book"
    template_name = "books/catalog_detail.html"

    def get_queryset(self):
        return CatalogBook.objects.prefetch_related("categories")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["shelf_book"] = Book.objects.filter(
                owner=self.request.user,
                catalog_book=self.object,
            ).first()
        try:
            context["forum"] = self.object.forum
        except Forum.DoesNotExist:
            context["forum"] = None
        return context


class BookSearchView(LoginRequiredMixin, TemplateView):
    template_name = "books/book_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        context["search_query"] = query
        if query:
            try:
                context["results"] = search_open_library(query)
            except BookSearchError as exc:
                context["search_error"] = str(exc)
        return context


class BookImportView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = load_import_token(request.POST.get("token", ""))
        except signing.BadSignature:
            messages.error(request, "This import result expired. Please search again.")
            return redirect("book-search")

        with transaction.atomic():
            candidates = CatalogBook.objects.none()
            if data.get("open_library_key"):
                candidates = CatalogBook.objects.filter(
                    open_library_key=data["open_library_key"]
                )
            if not candidates.exists() and data.get("isbn_13"):
                candidates = CatalogBook.objects.filter(isbn_13=data["isbn_13"])
            catalog_book = candidates.first()
            if not catalog_book:
                catalog_book = CatalogBook.objects.create(
                    title=data["title"],
                    author=data["author"],
                    isbn_10=data.get("isbn_10", ""),
                    isbn_13=data.get("isbn_13", ""),
                    open_library_key=data.get("open_library_key") or None,
                    cover_url=data.get("cover_url", ""),
                    publisher=data.get("publisher", ""),
                    published_year=data.get("published_year"),
                    added_by=request.user,
                )
                for name in data.get("categories", [])[:8]:
                    catalog_book.categories.add(
                        get_or_create_category(name, source=Category.Source.API)
                    )

            book, created = Book.objects.get_or_create(
                owner=request.user,
                catalog_book=catalog_book,
                defaults={
                    "title": catalog_book.title,
                    "author": catalog_book.author,
                    "status": request.POST.get("status", Book.ReadingStatus.WANT_TO_READ),
                },
            )
        if created:
            messages.success(request, f'“{book.title}” was added to your books.')
        else:
            messages.info(request, f'“{book.title}” is already in your books.')
        return redirect(book)


class CatalogBookAddToShelfView(LoginRequiredMixin, View):
    def post(self, request, pk):
        catalog_book = get_object_or_404(CatalogBook, pk=pk)
        book, created = Book.objects.get_or_create(
            owner=request.user,
            catalog_book=catalog_book,
            defaults={"title": catalog_book.title, "author": catalog_book.author},
        )
        messages.success(
            request,
            "Book added to your reading list." if created else "This book is already in your list.",
        )
        return redirect(book)


class CatalogBookCategoryAddView(LoginRequiredMixin, View):
    def post(self, request, pk):
        catalog_book = get_object_or_404(CatalogBook, pk=pk)
        names = parse_category_names(request.POST.get("categories", ""))
        for name in names:
            catalog_book.categories.add(get_or_create_category(name, request.user))
        if names:
            messages.success(request, "Categories added.")
        return redirect(catalog_book)


class StaffRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ForumCreateView(LoginRequiredMixin, CreateView):
    model = Forum
    form_class = ForumForm
    template_name = "forum/forum_form.html"

    def get_book(self):
        return get_object_or_404(CatalogBook, pk=self.kwargs["book_pk"])

    def dispatch(self, request, *args, **kwargs):
        book = self.get_book()
        if Forum.objects.filter(book=book).exists():
            return redirect(book.forum)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["title"] = f"{self.get_book().title} discussion"
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catalog_book"] = self.get_book()
        return context

    def form_valid(self, form):
        form.instance.book = self.get_book()
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ForumPermissionMixin(LoginRequiredMixin):
    model = Forum

    def get_queryset(self):
        queryset = Forum.objects.select_related("book", "created_by")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(created_by=self.request.user)


class ForumUpdateView(ForumPermissionMixin, UpdateView):
    form_class = ForumForm
    template_name = "forum/forum_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catalog_book"] = self.object.book
        return context


class ForumDeleteView(StaffRequiredMixin, DeleteView):
    model = Forum
    template_name = "forum/forum_confirm_delete.html"
    success_url = reverse_lazy("moderation-dashboard")


class ForumDetailView(DetailView):
    model = Forum
    context_object_name = "forum"
    template_name = "forum/forum_detail.html"

    def get_queryset(self):
        return Forum.objects.select_related("book", "created_by").prefetch_related(
            "posts__author", "posts__replies__author"
        )


class ForumPostCreateView(LoginRequiredMixin, CreateView):
    model = ForumPost
    form_class = ForumPostForm
    template_name = "forum/post_form.html"

    def get_forum(self):
        return get_object_or_404(Forum, pk=self.kwargs["forum_pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = self.get_forum()
        return context

    def form_valid(self, form):
        form.instance.forum = self.get_forum()
        form.instance.author = self.request.user
        return super().form_valid(form)


class ForumPostPermissionMixin(LoginRequiredMixin):
    model = ForumPost

    def get_queryset(self):
        queryset = ForumPost.objects.select_related("forum")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)


class ForumPostUpdateView(ForumPostPermissionMixin, UpdateView):
    form_class = ForumPostForm
    template_name = "forum/post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = self.object.forum
        return context


class ForumPostDeleteView(ForumPostPermissionMixin, DeleteView):
    template_name = "forum/post_confirm_delete.html"

    def get_success_url(self):
        return self.object.forum.get_absolute_url()


class ForumReplyCreateView(LoginRequiredMixin, CreateView):
    model = ForumReply
    form_class = ForumReplyForm
    template_name = "forum/reply_form.html"

    def get_post(self):
        return get_object_or_404(
            ForumPost.objects.select_related("forum"),
            pk=self.kwargs["post_pk"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.get_post()
        return context

    def form_valid(self, form):
        form.instance.post = self.get_post()
        form.instance.author = self.request.user
        return super().form_valid(form)


class ForumReplyPermissionMixin(LoginRequiredMixin):
    model = ForumReply

    def get_queryset(self):
        queryset = ForumReply.objects.select_related("post__forum")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)


class ForumReplyUpdateView(ForumReplyPermissionMixin, UpdateView):
    form_class = ForumReplyForm
    template_name = "forum/reply_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.object.post
        return context


class ForumReplyDeleteView(ForumReplyPermissionMixin, DeleteView):
    template_name = "forum/reply_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class ModerationDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "moderation/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forums"] = Forum.objects.select_related(
            "book", "created_by"
        ).annotate(post_count=Count("posts"))
        context["recent_posts"] = ForumPost.objects.select_related(
            "forum", "author"
        )[:20]
        context["recent_replies"] = ForumReply.objects.select_related(
            "post__forum", "author"
        )[:20]
        context["categories"] = Category.objects.select_related(
            "created_by"
        ).annotate(book_count=Count("books"))
        context["forum_count"] = Forum.objects.count()
        context["post_count"] = ForumPost.objects.count()
        context["reply_count"] = ForumReply.objects.count()
        context["category_count"] = Category.objects.count()
        return context


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "books/category_form.html"
    success_url = reverse_lazy("catalog-book-list")


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = "books/category_confirm_delete.html"
    success_url = reverse_lazy("catalog-book-list")
