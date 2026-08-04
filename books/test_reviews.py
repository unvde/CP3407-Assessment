from datetime import date
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Book


class CompletionReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")

    def completed_book(self, **overrides):
        values = {
            "owner": self.user,
            "title": "Dune",
            "author": "Frank Herbert",
            "status": Book.ReadingStatus.COMPLETED,
        }
        values.update(overrides)
        return Book(**values)

    @patch("books.models.timezone.localdate", return_value=date.max)
    def test_completed_book_retains_valid_review_data(self, mocked_localdate):
        book = self.completed_book(
            rating=5,
            completion_date=date.max,
            reflection="A thoughtful reflection.",
        )

        book.full_clean()

        self.assertEqual(book.rating, 5)
        self.assertEqual(book.completion_date, date.max)
        self.assertEqual(book.reflection, "A thoughtful reflection.")
        mocked_localdate.assert_called_once_with()

    def test_rating_must_be_between_one_and_five(self):
        for rating in (0, 6):
            with self.subTest(rating=rating):
                book = self.completed_book(rating=rating)
                with self.assertRaises(ValidationError):
                    book.full_clean()

    @patch("books.models.timezone.localdate", return_value=date.min)
    def test_completion_date_cannot_be_in_the_future(self, mocked_localdate):
        book = self.completed_book(completion_date=date.max)

        with self.assertRaises(ValidationError):
            book.full_clean()

        mocked_localdate.assert_called_once_with()

    def test_review_data_requires_completed_status(self):
        book = Book(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
            status=Book.ReadingStatus.CURRENTLY_READING,
            rating=4,
            reflection="Not finished yet.",
        )

        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_reflection_enforces_length_boundary(self):
        boundary_book = self.completed_book(reflection="x" * 1000)
        boundary_book.full_clean()

        over_limit_book = self.completed_book(reflection="x" * 1001)
        with self.assertRaises(ValidationError):
            over_limit_book.full_clean()


class CompletionReviewAcceptanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
            status=Book.ReadingStatus.COMPLETED,
        )
        self.active_book = Book.objects.create(
            owner=self.user,
            title="The Left Hand of Darkness",
            author="Ursula K. Le Guin",
            status=Book.ReadingStatus.CURRENTLY_READING,
        )
        self.other_book = Book.objects.create(
            owner=self.other_user,
            title="Beloved",
            author="Toni Morrison",
            status=Book.ReadingStatus.COMPLETED,
        )
        self.client.force_login(self.user)

    @patch("books.forms.timezone.localdate", return_value=date.max)
    def test_reader_can_add_review_to_completed_owned_book(self, mocked_localdate):
        response = self.client.post(
            reverse("book-review", args=[self.book.pk]),
            {
                "rating": 5,
                "completion_date": date.min.isoformat(),
                "reflection": "A lasting favourite.",
            },
        )

        self.book.refresh_from_db()
        self.assertEqual(self.book.rating, 5)
        self.assertEqual(self.book.completion_date, date.min)
        self.assertEqual(self.book.reflection, "A lasting favourite.")
        self.assertRedirects(response, self.book.get_absolute_url())
        self.assertEqual(mocked_localdate.call_count, 2)

    @patch("books.forms.timezone.localdate", return_value=date.max)
    def test_reader_can_update_existing_review(self, mocked_localdate):
        self.book.rating = 3
        self.book.completion_date = date.min
        self.book.reflection = "First thoughts."
        self.book.save()

        response = self.client.post(
            reverse("book-review", args=[self.book.pk]),
            {
                "rating": 4,
                "completion_date": date.min.isoformat(),
                "reflection": "Updated thoughts.",
            },
        )

        self.book.refresh_from_db()
        self.assertEqual(self.book.rating, 4)
        self.assertEqual(self.book.reflection, "Updated thoughts.")
        self.assertRedirects(response, self.book.get_absolute_url())
        self.assertEqual(mocked_localdate.call_count, 2)

    def test_non_completed_book_cannot_use_review_workflow(self):
        response = self.client.post(
            reverse("book-review", args=[self.active_book.pk]),
            {"rating": 4, "completion_date": "", "reflection": "Too early."},
        )

        self.assertEqual(response.status_code, 404)

    def test_reader_cannot_review_another_readers_book(self):
        response = self.client.post(
            reverse("book-review", args=[self.other_book.pk]),
            {"rating": 1, "completion_date": "", "reflection": "Intrusion"},
        )

        self.assertEqual(response.status_code, 404)
        self.other_book.refresh_from_db()
        self.assertIsNone(self.other_book.rating)

    def test_completed_book_detail_displays_private_review(self):
        self.book.rating = 5
        self.book.completion_date = date.min
        self.book.reflection = "Review insight visible only to the owner"
        self.book.save()
        self.other_book.rating = 1
        self.other_book.reflection = "Another reader's review insight"
        self.other_book.save()

        response = self.client.get(self.book.get_absolute_url())

        self.assertContains(response, "Review insight visible only to the owner")
        self.assertNotContains(response, "Another reader's review insight")

    def test_anonymous_reader_is_redirected_from_review_workflow(self):
        self.client.logout()
        route = reverse("book-review", args=[self.book.pk])

        response = self.client.get(route)

        self.assertRedirects(response, f"{reverse('login')}?next={route}")
