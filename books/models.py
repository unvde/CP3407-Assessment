from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    class Source(models.TextChoices):
        API = "api", "Book API"
        USER = "user", "User created"

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    source = models.CharField(
        max_length=10,
        choices=Source.choices,
        default=Source.USER,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_categories",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError({"name": "Category name cannot be blank."})

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        if not self.slug:
            base = slugify(self.name)[:80] or "category"
            slug = base
            counter = 2
            while Category.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class CatalogBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn_10 = models.CharField(max_length=10, blank=True, db_index=True)
    isbn_13 = models.CharField(max_length=13, blank=True, db_index=True)
    open_library_key = models.CharField(
        max_length=40,
        blank=True,
        unique=True,
        null=True,
    )
    cover_url = models.URLField(blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    published_year = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, max_length=3000)
    categories = models.ManyToManyField(Category, blank=True, related_name="books")
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="catalog_books_added",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "author"]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("catalog-book-detail", kwargs={"pk": self.pk})


class Book(models.Model):
    class ReadingStatus(models.TextChoices):
        WANT_TO_READ = "want_to_read", "Want to Read"
        CURRENTLY_READING = "currently_reading", "Currently Reading"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books",
    )
    catalog_book = models.ForeignKey(
        CatalogBook,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="shelf_entries",
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=ReadingStatus.choices,
        default=ReadingStatus.WANT_TO_READ,
    )
    total_pages = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    current_page = models.PositiveIntegerField(default=0, blank=True)
    target_date = models.DateField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    completion_date = models.DateField(null=True, blank=True)
    reflection = models.TextField(
        blank=True,
        max_length=1000,
        validators=[MaxLengthValidator(1000)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "title"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "catalog_book"],
                condition=models.Q(catalog_book__isnull=False),
                name="unique_catalog_book_per_owner",
            )
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})

    def clean(self):
        super().clean()
        self.reflection = self.reflection.strip()
        if (
            self.total_pages is not None
            and self.current_page is not None
            and self.current_page > self.total_pages
        ):
            raise ValidationError(
                {"current_page": "Current page cannot exceed total pages."}
            )
        has_review = any(
            (
                self.rating is not None,
                self.completion_date is not None,
                bool(self.reflection),
            )
        )
        if has_review and self.status != self.ReadingStatus.COMPLETED:
            raise ValidationError(
                {"status": "Only completed books can have a review."}
            )
        if (
            self.completion_date
            and self.completion_date > timezone.localdate()
        ):
            raise ValidationError(
                {"completion_date": "Completion date cannot be in the future."}
            )

    @property
    def progress_percentage(self):
        if not self.total_pages:
            return None
        return round((self.current_page / self.total_pages) * 100)


class ReadingNote(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(content=""),
                name="reading_note_content_not_empty",
            )
        ]

    def __str__(self):
        return f"Note for {self.book}"

    def clean(self):
        super().clean()
        self.content = self.content.strip()
        if not self.content:
            raise ValidationError(
                {"content": "Note content cannot be blank."}
            )


class Forum(models.Model):
    book = models.OneToOneField(
        CatalogBook,
        on_delete=models.CASCADE,
        related_name="forum",
    )
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True, max_length=500)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="forums_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("forum-detail", kwargs={"pk": self.pk})


class ForumPost(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="forum_posts",
    )
    title = models.CharField(max_length=180)
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        self.title = self.title.strip()
        self.content = self.content.strip()
        errors = {}
        if not self.title:
            errors["title"] = "Post title cannot be blank."
        if not self.content:
            errors["content"] = "Post content cannot be blank."
        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return f"{self.forum.get_absolute_url()}#post-{self.pk}"
