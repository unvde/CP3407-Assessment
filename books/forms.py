from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book


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
        fields = ("title", "author", "status", "total_pages")
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": True}),
            "total_pages": forms.NumberInput(attrs={"min": 1}),
        }

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_author(self):
        return self.cleaned_data["author"].strip()

