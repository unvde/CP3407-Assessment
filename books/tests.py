from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import BookForm, RegistrationForm
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

    def test_registration_requires_email(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "reader",
                "email": "",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "email", "This field is required.")
        self.assertFalse(User.objects.filter(username="reader").exists())

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "reader",
                "email": "reader@example.com",
                "password1": "StrongPass123!",
                "password2": "DifferentPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "password2",
            "The two password fields didn’t match.",
        )
        self.assertFalse(User.objects.filter(username="reader").exists())


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

    def test_private_book_routes_require_login(self):
        book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
        )
        routes = [
            reverse("book-add"),
            reverse("book-detail", args=[book.pk]),
            reverse("book-edit", args=[book.pk]),
            reverse("book-delete", args=[book.pk]),
        ]

        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertRedirects(response, f"{reverse('login')}?next={route}")


class BookModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reader",
            password="StrongPass123!",
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

    def test_default_status_is_want_to_read(self):
        book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
        )

        self.assertEqual(book.status, Book.ReadingStatus.WANT_TO_READ)

    def test_deleting_owner_cascades_to_books(self):
        book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
        )

        self.user.delete()

        self.assertFalse(Book.objects.filter(pk=book.pk).exists())


class BookFormTests(TestCase):
    def test_form_trims_title_and_author(self):
        form = BookForm(
            data={
                "title": "  Dune  ",
                "author": "  Frank Herbert  ",
                "status": Book.ReadingStatus.WANT_TO_READ,
                "total_pages": 412,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Dune")
        self.assertEqual(form.cleaned_data["author"], "Frank Herbert")

    def test_form_rejects_unknown_status(self):
        form = BookForm(
            data={
                "title": "Dune",
                "author": "Frank Herbert",
                "status": "abandoned",
                "total_pages": 412,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)


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


class ReadingProgressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
            status=Book.ReadingStatus.CURRENTLY_READING,
            total_pages=400,
            current_page=100,
        )
        self.client.force_login(self.user)

    def test_progress_percentage_is_calculated(self):
        self.assertEqual(self.book.progress_percentage, 25)

    def test_percentage_is_unavailable_without_total_pages(self):
        self.book.total_pages = None

        self.assertIsNone(self.book.progress_percentage)

    def test_current_page_cannot_exceed_total_pages(self):
        self.book.current_page = 401

        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_update_saves_valid_current_page(self):
        response = self.client.post(
            reverse("book-edit", args=[self.book.pk]),
            {
                "title": self.book.title,
                "author": self.book.author,
                "status": self.book.status,
                "total_pages": 400,
                "current_page": 240,
            },
        )

        self.book.refresh_from_db()
        self.assertRedirects(response, self.book.get_absolute_url())
        self.assertEqual(self.book.current_page, 240)


class ReadingDashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.active_book = Book.objects.create(
            owner=self.user,
            title="Active Book",
            author="A Reader",
            status=Book.ReadingStatus.CURRENTLY_READING,
            total_pages=200,
            current_page=50,
        )
        Book.objects.create(
            owner=self.user,
            title="Future Book",
            author="A Reader",
            status=Book.ReadingStatus.WANT_TO_READ,
        )
        Book.objects.create(
            owner=self.other_user,
            title="Private Active Book",
            author="Other Reader",
            status=Book.ReadingStatus.CURRENTLY_READING,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
        )

    def test_dashboard_contains_only_currently_reading_books(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "Active Book")
        self.assertNotContains(response, "Future Book")

    def test_dashboard_does_not_reveal_other_users_books(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertNotContains(response, "Private Active Book")


class ReadingPlanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
            status=Book.ReadingStatus.CURRENTLY_READING,
            total_pages=400,
        )
        self.other_book = Book.objects.create(
            owner=self.other_user,
            title="Private Plan",
            author="Other Reader",
        )
        self.client.force_login(self.user)

    def book_data(self, target_date=""):
        return {
            "title": self.book.title,
            "author": self.book.author,
            "status": self.book.status,
            "total_pages": self.book.total_pages,
            "current_page": self.book.current_page,
            "target_date": target_date,
        }

    def test_reader_can_add_future_target(self):
        target = timezone.localdate() + timedelta(days=7)
        response = self.client.post(
            reverse("book-edit", args=[self.book.pk]),
            self.book_data(target.isoformat()),
        )
        self.book.refresh_from_db()
        self.assertRedirects(response, self.book.get_absolute_url())
        self.assertEqual(self.book.target_date, target)

    def test_new_past_target_is_rejected(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        response = self.client.post(
            reverse("book-edit", args=[self.book.pk]),
            self.book_data(yesterday.isoformat()),
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "target_date",
            "Target date cannot be in the past.",
        )
        self.book.refresh_from_db()
        self.assertIsNone(self.book.target_date)

    def test_reader_can_remove_target(self):
        self.book.target_date = timezone.localdate() + timedelta(days=7)
        self.book.save()
        self.client.post(
            reverse("book-edit", args=[self.book.pk]),
            self.book_data(""),
        )
        self.book.refresh_from_db()
        self.assertIsNone(self.book.target_date)

    def test_reader_cannot_change_another_users_target(self):
        target = timezone.localdate() + timedelta(days=7)
        response = self.client.post(
            reverse("book-edit", args=[self.other_book.pk]),
            {
                "title": self.other_book.title,
                "author": self.other_book.author,
                "status": self.other_book.status,
                "total_pages": "",
                "current_page": 0,
                "target_date": target.isoformat(),
            },
        )
        self.assertEqual(response.status_code, 404)
        self.other_book.refresh_from_db()
        self.assertIsNone(self.other_book.target_date)
