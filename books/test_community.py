import io
import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Book, CatalogBook, Category, Forum, ForumPost
from .services import BookSearchResult, search_open_library


class OpenLibraryServiceTests(TestCase):
    @patch("books.services.urlopen")
    def test_search_parses_results_using_explicit_certificate_context(self, urlopen):
        urlopen.return_value = io.BytesIO(
            json.dumps(
                {
                    "docs": [
                        {
                            "key": "/works/OL893415W",
                            "title": "Dune",
                            "author_name": ["Frank Herbert"],
                            "isbn": ["9780441172719"],
                            "cover_i": 123,
                            "publisher": ["Ace"],
                            "first_publish_year": 1965,
                            "subject": ["Science fiction", "Adventure"],
                        }
                    ]
                }
            ).encode()
        )

        results = search_open_library("Dune")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Dune")
        self.assertEqual(results[0].isbn_13, "9780441172719")
        self.assertEqual(results[0].categories, ("Science fiction", "Adventure"))
        _, kwargs = urlopen.call_args
        self.assertEqual(kwargs["timeout"], 8)
        self.assertIsNotNone(kwargs["context"])


class BookImportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.client.force_login(self.user)
        self.result = BookSearchResult(
            title="Dune",
            author="Frank Herbert",
            open_library_key="OL893415W",
            isbn_13="9780441172719",
            cover_url="https://covers.openlibrary.org/b/id/1-M.jpg",
            publisher="Ace",
            published_year=1965,
            categories=("Science fiction", "Adventure"),
        )

    @patch("books.views.search_open_library")
    def test_search_displays_api_results(self, search):
        search.return_value = [self.result]

        response = self.client.get(reverse("book-search"), {"q": "Dune"})

        self.assertContains(response, "Dune")
        self.assertContains(response, "9780441172719")
        search.assert_called_once_with("Dune")

    def test_import_creates_catalog_book_shelf_entry_and_categories(self):
        response = self.client.post(
            reverse("book-import"),
            {"token": self.result.import_token},
        )

        catalog_book = CatalogBook.objects.get(open_library_key="OL893415W")
        shelf_book = Book.objects.get(owner=self.user, catalog_book=catalog_book)
        self.assertRedirects(response, shelf_book.get_absolute_url())
        self.assertEqual(catalog_book.isbn_13, "9780441172719")
        self.assertSetEqual(
            set(catalog_book.categories.values_list("name", flat=True)),
            {"Science fiction", "Adventure"},
        )

    def test_duplicate_import_reuses_catalog_and_shelf_entry(self):
        for _ in range(2):
            self.client.post(reverse("book-import"), {"token": self.result.import_token})

        self.assertEqual(CatalogBook.objects.count(), 1)
        self.assertEqual(Book.objects.filter(owner=self.user).count(), 1)

    def test_tampered_import_token_is_rejected(self):
        response = self.client.post(
            reverse("book-import"),
            {"token": self.result.import_token + "tampered"},
        )

        self.assertRedirects(response, reverse("book-search"))
        self.assertFalse(CatalogBook.objects.exists())


class ForumPermissionTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="pass")
        self.other = User.objects.create_user(username="other", password="pass")
        self.staff = User.objects.create_user(
            username="moderator", password="pass", is_staff=True
        )
        self.book = CatalogBook.objects.create(title="Dune", author="Frank Herbert")
        self.forum = Forum.objects.create(
            book=self.book,
            title="Dune discussion",
            created_by=self.author,
        )
        self.post = ForumPost.objects.create(
            forum=self.forum,
            author=self.author,
            title="The ecology of Arrakis",
            content="A discussion of water and power.",
        )

    def test_forum_is_public_but_posting_requires_login(self):
        self.assertContains(self.client.get(self.forum.get_absolute_url()), self.post.title)
        add_url = reverse("forum-post-add", args=[self.forum.pk])
        self.assertRedirects(
            self.client.get(add_url),
            f"{reverse('login')}?next={add_url}",
        )

    def test_author_can_edit_own_post(self):
        self.client.force_login(self.author)
        response = self.client.post(
            reverse("forum-post-edit", args=[self.post.pk]),
            {"title": "Updated title", "content": self.post.content},
        )

        self.post.refresh_from_db()
        self.assertRedirects(response, self.post.get_absolute_url())
        self.assertEqual(self.post.title, "Updated title")

    def test_other_user_cannot_edit_post(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("forum-post-edit", args=[self.post.pk]),
            {"title": "Hijacked", "content": "Changed"},
        )

        self.assertEqual(response.status_code, 404)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, "Hijacked")

    def test_staff_can_delete_any_post(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse("forum-post-delete", args=[self.post.pk]))

        self.assertRedirects(response, self.forum.get_absolute_url())
        self.assertFalse(ForumPost.objects.filter(pk=self.post.pk).exists())


class CategoryModerationTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username="reader", password="pass")
        self.staff = User.objects.create_user(
            username="staff", password="pass", is_staff=True
        )
        self.book = CatalogBook.objects.create(title="Dune", author="Frank Herbert")
        self.category = Category.objects.create(name="Sci Fi", created_by=self.reader)
        self.book.categories.add(self.category)

    def test_reader_can_add_free_text_category(self):
        self.client.force_login(self.reader)
        self.client.post(
            reverse("catalog-category-add", args=[self.book.pk]),
            {"categories": "Politics, Desert ecology"},
        )

        self.assertTrue(self.book.categories.filter(name="Politics").exists())
        self.assertTrue(self.book.categories.filter(name="Desert ecology").exists())

    def test_non_staff_cannot_rename_category(self):
        self.client.force_login(self.reader)
        response = self.client.post(
            reverse("category-edit", args=[self.category.pk]),
            {"name": "Science fiction"},
        )

        self.assertEqual(response.status_code, 403)

    def test_staff_can_rename_and_delete_category(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            reverse("category-edit", args=[self.category.pk]),
            {"name": "Science fiction"},
        )
        self.assertRedirects(response, reverse("catalog-book-list"))
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Science fiction")

        self.client.post(reverse("category-delete", args=[self.category.pk]))
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())
