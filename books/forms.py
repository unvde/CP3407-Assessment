from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Book, Category, Forum, ForumPost, ReadingNote


def parse_category_names(value):
    names = []
    seen = set()
    for raw_name in value.replace("，", ",").split(","):
        name = raw_name.strip()
        key = name.casefold()
        if name and key not in seen:
            names.append(name[:80])
            seen.add(key)
    return names


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
    categories = forms.CharField(
        required=False,
        max_length=500,
        label="Categories",
        help_text="Optional. Separate categories with commas, for example: Science fiction, Adventure.",
        widget=forms.TextInput(attrs={"placeholder": "Science fiction, Romance"}),
    )

    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "status",
            "total_pages",
            "current_page",
            "target_date",
            "categories",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.catalog_book_id:
            self.fields["categories"].initial = ", ".join(
                self.instance.catalog_book.categories.values_list("name", flat=True)
            )

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

    def clean_categories(self):
        return parse_category_names(self.cleaned_data.get("categories", ""))


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ("title", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_description(self):
        return self.cleaned_data["description"].strip()


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ("title", "content")
        widgets = {"content": forms.Textarea(attrs={"rows": 9})}

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_content(self):
        return self.cleaned_data["content"].strip()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        duplicate = Category.objects.filter(name__iexact=name).exclude(
            pk=self.instance.pk
        )
        if duplicate.exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name


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


class CompletionReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={"min": 1, "max": 5, "autofocus": True}),
        help_text="Choose a rating from 1 to 5.",
    )
    completion_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    reflection = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={"rows": 8}),
        help_text="Up to 1000 characters.",
    )

    class Meta:
        model = Book
        fields = ("rating", "completion_date", "reflection")

    def clean_completion_date(self):
        completion_date = self.cleaned_data["completion_date"]
        if completion_date > timezone.localdate():
            raise forms.ValidationError(
                "Completion date cannot be in the future."
            )
        return completion_date

    def clean_reflection(self):
        return self.cleaned_data["reflection"].strip()
