from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Book,
    Category,
    Forum,
    ForumPost,
    ForumReply,
    PublicReview,
    ReadingList,
    ReadingNote,
)


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
            "categories",
        )
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": True}),
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

    def clean_categories(self):
        return parse_category_names(self.cleaned_data.get("categories", ""))


class PublicReviewForm(forms.ModelForm):
    class Meta:
        model = PublicReview
        fields = ("rating", "content")
        labels = {"content": "Your review"}
        widgets = {
            "rating": forms.RadioSelect(
                choices=[
                    (value, f"{value} star{'s' if value != 1 else ''}")
                    for value in range(1, 6)
                ]
            ),
            "content": forms.Textarea(
                attrs={
                    "rows": 8,
                    "placeholder": "What should other readers know about this book?",
                }
            ),
        }

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if not content:
            raise forms.ValidationError("Review cannot be blank.")
        return content


class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ("name", "description", "is_public")
        labels = {"is_public": "Make this list public"}
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_description(self):
        return self.cleaned_data["description"].strip()


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


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ("content",)
        labels = {"content": "Reply"}
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Add to the discussion…",
                }
            )
        }

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
