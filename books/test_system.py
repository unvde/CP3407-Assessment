from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Book, ReadingNote


class IterationThreeSystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")

    def test_reader_journey_combines_search_notes_and_completion_review(self):
        self.client.force_login(self.user)
        create_response = self.client.post(
            reverse("book-add"),
            {
                "title": "Dune",
                "author": "Frank Herbert",
                "status": Book.ReadingStatus.WANT_TO_READ,
                "total_pages": 412,
                "current_page": 0,
                "target_date": "",
            },
        )
        book = Book.objects.get(owner=self.user, title="Dune")
        self.assertRedirects(create_response, book.get_absolute_url())

        search_response = self.client.get(
            reverse("book-list"),
            {"q": "dune", "status": Book.ReadingStatus.WANT_TO_READ},
        )
        self.assertQuerySetEqual(search_response.context["books"], [book])

        complete_response = self.client.post(
            reverse("book-edit", args=[book.pk]),
            {
                "title": book.title,
                "author": book.author,
                "status": Book.ReadingStatus.COMPLETED,
                "total_pages": 412,
                "current_page": 412,
                "target_date": "",
            },
        )
        self.assertRedirects(complete_response, book.get_absolute_url())

        note_response = self.client.post(
            reverse("note-add", args=[book.pk]),
            {"content": "A private system-test note."},
        )
        self.assertRedirects(note_response, book.get_absolute_url())

        review_response = self.client.post(
            reverse("book-review", args=[book.pk]),
            {
                "rating": 5,
                "completion_date": date.min.isoformat(),
                "reflection": "A private system-test review.",
            },
        )
        self.assertRedirects(review_response, book.get_absolute_url())

        detail_response = self.client.get(book.get_absolute_url())
        self.assertContains(detail_response, "A private system-test note.")
        self.assertContains(detail_response, "A private system-test review.")
        self.assertContains(detail_response, "5 / 5")

        completed_response = self.client.get(
            reverse("book-list"),
            {"status": Book.ReadingStatus.COMPLETED},
        )
        self.assertQuerySetEqual(completed_response.context["books"], [book])

    def test_owner_boundary_protects_combined_iteration_three_features(self):
        other_book = Book.objects.create(
            owner=self.other_user,
            title="Beloved",
            author="Toni Morrison",
            status=Book.ReadingStatus.COMPLETED,
        )
        other_note = ReadingNote.objects.create(
            book=other_book,
            content="Another reader's system-test note.",
        )
        self.client.force_login(self.user)

        list_response = self.client.get(reverse("book-list"), {"q": "beloved"})
        self.assertQuerySetEqual(list_response.context["books"], [])
        self.assertEqual(
            self.client.get(other_book.get_absolute_url()).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(
                reverse("note-add", args=[other_book.pk]),
                {"content": "Intrusion"},
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(
                reverse("note-edit", args=[other_note.pk]),
                {"content": "Changed"},
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(reverse("note-delete", args=[other_note.pk])).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(
                reverse("book-review", args=[other_book.pk]),
                {
                    "rating": 1,
                    "completion_date": date.min.isoformat(),
                    "reflection": "Intrusion",
                },
            ).status_code,
            404,
        )

        other_note.refresh_from_db()
        other_book.refresh_from_db()
        self.assertEqual(other_note.content, "Another reader's system-test note.")
        self.assertIsNone(other_book.rating)

    def test_anonymous_reader_is_redirected_from_iteration_three_writes(self):
        book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
            status=Book.ReadingStatus.COMPLETED,
        )
        note = ReadingNote.objects.create(book=book, content="Private note")
        routes = [
            reverse("note-add", args=[book.pk]),
            reverse("note-edit", args=[note.pk]),
            reverse("note-delete", args=[note.pk]),
            reverse("book-review", args=[book.pk]),
        ]

        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertRedirects(response, f"{reverse('login')}?next={route}")
