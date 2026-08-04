from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from .models import (
    Book,
    CatalogBook,
    Category,
    PublicReview,
    ReadingList,
    RecommendationDismissal,
)
from .services import BookSearchResult


class ReadingListTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass")
        self.other = User.objects.create_user(username="other", password="pass")
        self.book = CatalogBook.objects.create(title="Dune", author="Frank Herbert")
        self.public_list = ReadingList.objects.create(
            owner=self.owner,
            name="Favourite science fiction",
            is_public=True,
        )
        self.private_list = ReadingList.objects.create(
            owner=self.owner,
            name="Private ideas",
            is_public=False,
        )

    def test_owner_can_create_list_and_add_and_remove_book(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("reading-list-book-add", args=[self.public_list.pk, self.book.pk])
        )
        self.assertRedirects(response, self.book.get_absolute_url())
        self.assertTrue(self.public_list.books.filter(pk=self.book.pk).exists())

        response = self.client.post(
            reverse("reading-list-book-remove", args=[self.public_list.pk, self.book.pk])
        )
        self.assertRedirects(response, self.public_list.get_absolute_url())
        self.assertFalse(self.public_list.books.filter(pk=self.book.pk).exists())

    def test_other_reader_cannot_modify_list(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("reading-list-book-add", args=[self.public_list.pk, self.book.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_public_list_is_visible_but_private_list_is_not(self):
        self.assertEqual(self.client.get(self.public_list.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(self.private_list.get_absolute_url()).status_code, 404)

        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.private_list.get_absolute_url()).status_code, 200)


class RecommendationTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username="reader", password="pass")
        science_fiction = Category.objects.create(name="Science fiction")
        owned_catalog = CatalogBook.objects.create(title="Dune", author="Frank Herbert")
        owned_catalog.categories.add(science_fiction)
        self.recommended = CatalogBook.objects.create(
            title="The Left Hand of Darkness",
            author="Ursula K. Le Guin",
        )
        self.recommended.categories.add(science_fiction)
        self.unrelated = CatalogBook.objects.create(title="Emma", author="Jane Austen")
        Book.objects.create(
            owner=self.reader,
            catalog_book=owned_catalog,
            title=owned_catalog.title,
            author=owned_catalog.author,
        )
        PublicReview.objects.create(
            catalog_book=owned_catalog,
            author=self.reader,
            rating=5,
            content="A favourite.",
        )

    @patch("books.views.search_open_library", return_value=[])
    def test_dashboard_recommends_matching_categories_not_owned_books(self, _search):
        self.client.force_login(self.reader)
        response = self.client.get(reverse("dashboard"))

        self.assertContains(response, self.recommended.title)
        self.assertNotContains(response, self.unrelated.title)
        self.assertContains(response, "Because you like Science fiction")

    def test_not_interested_hides_local_recommendation(self):
        self.client.force_login(self.reader)
        self.client.post(
            reverse("recommendation-dismiss"),
            {"identifier": f"catalog:{self.recommended.pk}"},
        )

        self.assertTrue(
            RecommendationDismissal.objects.filter(
                user=self.reader,
                identifier=f"catalog:{self.recommended.pk}",
            ).exists()
        )
        with patch("books.views.search_open_library", return_value=[]):
            response = self.client.get(reverse("dashboard"))
        self.assertNotContains(response, self.recommended.title)

    @patch("books.views.search_open_library")
    def test_api_fallback_fills_sparse_recommendations(self, search):
        search.return_value = [
            BookSearchResult(
                title="A Memory Called Empire",
                author="Arkady Martine",
                open_library_key="OL-FALLBACK",
                categories=("Science fiction",),
            )
        ]
        self.client.force_login(self.reader)

        response = self.client.get(reverse("dashboard"))

        self.assertContains(response, "A Memory Called Empire")
        self.assertContains(response, "From Open Library")


class PublicDiscoveryTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username="curator", password="pass")
        self.book = CatalogBook.objects.create(title="Dune", author="Frank Herbert")
        self.public_list = ReadingList.objects.create(
            owner=self.reader,
            name="Desert science fiction",
            description="Books about ecology and power.",
            is_public=True,
        )
        self.public_list.books.add(self.book)
        self.private_list = ReadingList.objects.create(
            owner=self.reader, name="Secret drafts", is_public=False
        )
        PublicReview.objects.create(
            catalog_book=self.book,
            author=self.reader,
            rating=5,
            content="A classic.",
        )

    def test_public_list_discovery_searches_books_and_hides_private_lists(self):
        response = self.client.get(reverse("public-list-list"), {"q": "Dune"})

        self.assertContains(response, self.public_list.name)
        self.assertNotContains(response, self.private_list.name)

    def test_public_profile_shows_lists_and_reviews_but_not_private_lists(self):
        response = self.client.get(
            reverse("public-profile", args=[self.reader.username])
        )

        self.assertContains(response, self.public_list.name)
        self.assertContains(response, "A classic.")
        self.assertNotContains(response, self.private_list.name)


class CategoryBrowseTests(TestCase):
    def setUp(self):
        science_fiction = Category.objects.create(name="Science Fiction")
        romance = Category.objects.create(name="Romance")
        self.dune = CatalogBook.objects.create(title="Dune", author="Frank Herbert")
        self.emma = CatalogBook.objects.create(title="Emma", author="Jane Austen")
        self.dune.categories.add(science_fiction)
        self.emma.categories.add(romance)
        self.science_fiction = science_fiction

    @patch("books.views.search_open_library_subject")
    def test_trait_search_uses_api_and_shows_pagination(self, search):
        search.return_value = [
            BookSearchResult(
                title=f"Science Fiction Book {number}",
                author="Demo Author",
                open_library_key=f"OL-SF-{number}",
                categories=("Science Fiction",),
            )
            for number in range(10)
        ]
        response = self.client.get(
            reverse("catalog-book-list"),
            {"trait": self.science_fiction.name, "page": 2},
        )

        self.assertContains(response, "Books with: Science Fiction")
        self.assertContains(response, "Science Fiction Book 0")
        self.assertNotContains(response, self.emma.title)
        self.assertContains(response, "Previous page")
        self.assertContains(response, "Next page")
        search.assert_called_once_with(
            "Science Fiction",
            limit=10,
            page=2,
        )


class DemoContentCommandTests(TestCase):
    def test_command_creates_demo_activity_idempotently(self):
        options = {
            "reader_password": "Reader-Test-Password-2026",
            "admin_password": "Admin-Test-Password-2026",
            "verbosity": 0,
        }
        call_command("seed_demo_content", **options)
        call_command("seed_demo_content", **options)

        self.assertEqual(
            User.objects.filter(username__startswith="demo_").count(), 4
        )
        self.assertTrue(
            User.objects.filter(
                username="reading_admin", is_staff=True, is_superuser=True
            ).exists()
        )
        self.assertEqual(CatalogBook.objects.count(), 10)
        self.assertEqual(ReadingList.objects.count(), 5)
        self.assertEqual(PublicReview.objects.count(), 8)
