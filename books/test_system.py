from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Book, CatalogBook, PublicReview, ReadingList


class CommunityDiscoverySystemTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username="reader", password="pass")
        self.other = User.objects.create_user(username="other", password="pass")
        self.catalog_book = CatalogBook.objects.create(
            title="Dune",
            author="Frank Herbert",
            isbn_13="9780441172719",
        )
        self.book = Book.objects.create(
            owner=self.reader,
            catalog_book=self.catalog_book,
            title="Dune",
            author="Frank Herbert",
        )
        self.client.force_login(self.reader)

    def test_reader_journey_updates_status_reviews_and_builds_list(self):
        self.client.post(
            reverse("book-status", args=[self.book.pk]),
            {"status": Book.ReadingStatus.COMPLETED},
        )
        self.client.post(
            reverse("public-review-upsert", args=[self.catalog_book.pk]),
            {"rating": 5, "content": "A lasting favourite."},
        )
        response = self.client.post(
            reverse("reading-list-create"),
            {
                "name": "Favourite science fiction",
                "description": "Books worth revisiting.",
                "is_public": True,
            },
        )
        reading_list = ReadingList.objects.get(owner=self.reader)
        self.client.post(
            reverse(
                "reading-list-book-add",
                args=[reading_list.pk, self.catalog_book.pk],
            )
        )

        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.ReadingStatus.COMPLETED)
        self.assertTrue(
            PublicReview.objects.filter(
                author=self.reader, catalog_book=self.catalog_book, rating=5
            ).exists()
        )
        self.assertTrue(reading_list.books.filter(pk=self.catalog_book.pk).exists())
        self.assertRedirects(response, reading_list.get_absolute_url())

    def test_reader_cannot_change_another_readers_status_or_private_list(self):
        other_book = Book.objects.create(
            owner=self.other,
            catalog_book=self.catalog_book,
            title="Dune",
            author="Frank Herbert",
        )
        private_list = ReadingList.objects.create(
            owner=self.other,
            name="Private",
        )

        self.assertEqual(
            self.client.post(
                reverse("book-status", args=[other_book.pk]),
                {"status": Book.ReadingStatus.COMPLETED},
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(private_list.get_absolute_url()).status_code,
            404,
        )

    def test_anonymous_reader_is_redirected_from_new_write_actions(self):
        self.client.logout()
        routes = [
            reverse("public-review-upsert", args=[self.catalog_book.pk]),
            reverse("reading-list-create"),
            reverse("book-status", args=[self.book.pk]),
        ]
        for route in routes:
            with self.subTest(route=route):
                self.assertRedirects(
                    self.client.get(route),
                    f"{reverse('login')}?next={route}",
                )
