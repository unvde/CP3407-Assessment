from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Book


class RegistrationTests(TestCase):
    def test_registration_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "reader",
                "email": "reader@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("book-list"))
        self.assertTrue(User.objects.filter(username="reader").exists())
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get().pk)

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(
            username="first",
            email="reader@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("register"),
            {
                "username": "second",
                "email": "READER@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An account already uses this email address.")
        self.assertFalse(User.objects.filter(username="second").exists())


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reader",
            password="StrongPass123!",
        )

    def test_valid_login(self):
        response = self.client.post(
            reverse("login"),
            {"username": "reader", "password": "StrongPass123!"},
        )

        self.assertRedirects(response, reverse("book-list"))

    def test_invalid_login(self):
        response = self.client.post(
            reverse("login"),
            {"username": "reader", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please enter a correct username and password",
        )

    def test_logout(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_book_list_requires_login(self):
        response = self.client.get(reverse("book-list"))

        expected = f"{reverse('login')}?next={reverse('book-list')}"
        self.assertRedirects(response, expected)


class BookModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reader",
            password="StrongPass123!",
        )

    def test_status_choices_are_iteration_one_values(self):
        values = {value for value, _label in Book.ReadingStatus.choices}

        self.assertEqual(
            values,
            {"want_to_read", "currently_reading", "paused", "completed"},
        )

    def test_total_pages_must_be_positive(self):
        book = Book(
            owner=self.user,
            title="A Book",
            author="An Author",
            total_pages=0,
        )

        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_string_representation(self):
        book = Book(title="Dune", author="Frank Herbert")

        self.assertEqual(str(book), "Dune by Frank Herbert")


class BookManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reader",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="StrongPass123!",
        )
        self.book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
            status=Book.ReadingStatus.WANT_TO_READ,
            total_pages=412,
        )
        self.other_book = Book.objects.create(
            owner=self.other_user,
            title="Beloved",
            author="Toni Morrison",
        )
        self.client.force_login(self.user)

    def test_list_contains_only_current_users_books(self):
        response = self.client.get(reverse("book-list"))

        self.assertContains(response, "Dune")
        self.assertNotContains(response, "Beloved")

    def test_create_book_assigns_authenticated_owner(self):
        response = self.client.post(
            reverse("book-add"),
            {
                "title": "The Left Hand of Darkness",
                "author": "Ursula K. Le Guin",
                "status": Book.ReadingStatus.CURRENTLY_READING,
                "total_pages": 304,
            },
        )

        created = Book.objects.get(title="The Left Hand of Darkness")
        self.assertEqual(created.owner, self.user)
        self.assertRedirects(response, created.get_absolute_url())

    def test_add_book_page_explains_reading_statuses(self):
        response = self.client.get(reverse("book-add"))

        self.assertContains(
            response,
            (
                "Want to Read: saved for future reading; "
                "Currently Reading: actively being read; "
                "Paused: temporarily stopped; "
                "Completed: finished."
            ),
        )

    def test_create_rejects_non_positive_page_count(self):
        response = self.client.post(
            reverse("book-add"),
            {
                "title": "Invalid Book",
                "author": "Example Author",
                "status": Book.ReadingStatus.WANT_TO_READ,
                "total_pages": 0,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "total_pages",
            "Ensure this value is greater than or equal to 1.",
        )
        self.assertFalse(Book.objects.filter(title="Invalid Book").exists())

    def test_update_book(self):
        response = self.client.post(
            reverse("book-edit", args=[self.book.pk]),
            {
                "title": self.book.title,
                "author": self.book.author,
                "status": Book.ReadingStatus.CURRENTLY_READING,
                "total_pages": self.book.total_pages,
            },
        )

        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.ReadingStatus.CURRENTLY_READING)
        self.assertRedirects(response, self.book.get_absolute_url())

    def test_delete_book(self):
        response = self.client.post(reverse("book-delete", args=[self.book.pk]))

        self.assertRedirects(response, reverse("book-list"))
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_cannot_view_another_users_book(self):
        response = self.client.get(
            reverse("book-detail", args=[self.other_book.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_cannot_edit_another_users_book(self):
        response = self.client.post(
            reverse("book-edit", args=[self.other_book.pk]),
            {
                "title": "Changed",
                "author": "Changed",
                "status": Book.ReadingStatus.COMPLETED,
                "total_pages": 100,
            },
        )

        self.assertEqual(response.status_code, 404)
        self.other_book.refresh_from_db()
        self.assertEqual(self.other_book.title, "Beloved")

    def test_cannot_delete_another_users_book(self):
        response = self.client.post(
            reverse("book-delete", args=[self.other_book.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Book.objects.filter(pk=self.other_book.pk).exists())
