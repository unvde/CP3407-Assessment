from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "title"]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})

    def clean(self):
        super().clean()
        if (
            self.total_pages is not None
            and self.current_page is not None
            and self.current_page > self.total_pages
        ):
            raise ValidationError(
                {"current_page": "Current page cannot exceed total pages."}
            )

    @property
    def progress_percentage(self):
        if not self.total_pages:
            return None
        return round((self.current_page / self.total_pages) * 100)
