from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
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



class PublicReview(models.Model):
    catalog_book = models.ForeignKey(
        CatalogBook,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="public_book_reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["catalog_book", "author"],
                name="one_public_review_per_book_and_author",
            )
        ]

    def __str__(self):
        return f"Review of {self.catalog_book}"

    def clean(self):
        super().clean()
        self.content = self.content.strip()
        if not self.content:
            raise ValidationError({"content": "Review cannot be blank."})

    def get_absolute_url(self):
        return f"{self.catalog_book.get_absolute_url()}#review-{self.pk}"


class ReadingList(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reading_lists",
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, max_length=500)
    is_public = models.BooleanField(default=False)
    books = models.ManyToManyField(
        CatalogBook,
        blank=True,
        related_name="reading_lists",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_reading_list_name_per_owner",
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("reading-list-detail", kwargs={"pk": self.pk})


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


class ForumReply(models.Model):
    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="forum_replies",
    )
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "forum replies"

    def __str__(self):
        return f"Reply to {self.post}"

    def clean(self):
        super().clean()
        self.content = self.content.strip()
        if not self.content:
            raise ValidationError({"content": "Reply content cannot be blank."})

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}-reply-{self.pk}"
