from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Book, ReadingNote


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account already uses this email address.")
        return email


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "status",
            "total_pages",
            "current_page",
            "target_date",
        )
        help_texts = {
            "status": (
                "Want to Read: saved for future reading; "
                "Currently Reading: actively being read; "
                "Paused: temporarily stopped; "
                "Completed: finished."
            ),
            "current_page": (
                "Enter 0 if you have not started. Progress cannot exceed the "
                "total page count when one is recorded."
            ),
            "target_date": "Optional. Choose today or a future date.",
        }
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": True}),
            "total_pages": forms.NumberInput(attrs={"min": 1}),
            "current_page": forms.NumberInput(attrs={"min": 0}),
            "target_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_author(self):
        return self.cleaned_data["author"].strip()

    def clean_current_page(self):
        return self.cleaned_data.get("current_page") or 0

    def clean_target_date(self):
        target_date = self.cleaned_data.get("target_date")
        original_target = (
            Book.objects.filter(pk=self.instance.pk)
            .values_list("target_date", flat=True)
            .first()
            if self.instance.pk
            else None
        )
        if (
            target_date
            and target_date < timezone.localdate()
            and target_date != original_target
        ):
            raise forms.ValidationError("Target date cannot be in the past.")
        return target_date


class ReadingNoteForm(forms.ModelForm):
    content = forms.CharField(
        label="Note",
        required=False,
        widget=forms.Textarea(
            attrs={
                "autofocus": True,
                "rows": 8,
                "placeholder": "Record an idea or observation from this book.",
            }
        ),
    )

    class Meta:
        model = ReadingNote
        fields = ("content",)

    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if not content:
            raise forms.ValidationError("Note content cannot be blank.")
        return content
