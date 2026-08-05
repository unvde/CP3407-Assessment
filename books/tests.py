from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

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

    def test_normal_reader_is_not_redirected_to_staff_page_after_login(self):
        response = self.client.post(
            f"{reverse('login')}?next={reverse('moderation-dashboard')}",
            {"username": "reader", "password": "StrongPass123!"},
            follow=True,
        )

        self.assertRedirects(response, reverse("book-list"))
        self.assertContains(
            response,
            "that page is only available to administrators",
        )

    def test_staff_user_can_continue_to_moderation_after_login(self):
        staff = User.objects.create_user(
            username="staff",
            password="StrongPass123!",
            is_staff=True,
        )
        response = self.client.post(
            f"{reverse('login')}?next={reverse('moderation-dashboard')}",
            {"username": staff.username, "password": "StrongPass123!"},
        )

        self.assertRedirects(response, reverse("moderation-dashboard"))

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
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Dune")
        self.assertEqual(form.cleaned_data["author"], "Frank Herbert")

    def test_form_does_not_expose_status_or_progress_fields(self):
        form = BookForm(
            data={
                "title": "Dune",
                "author": "Frank Herbert",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertNotIn("status", form.fields)
        self.assertNotIn("total_pages", form.fields)
        self.assertNotIn("current_page", form.fields)
        self.assertNotIn("target_date", form.fields)


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
                "categories": "Science fiction",
            },
        )

        self.book.refresh_from_db()
        self.assertEqual(self.book.status, Book.ReadingStatus.WANT_TO_READ)
        self.assertRedirects(response, self.book.get_absolute_url())

    def test_status_is_updated_from_my_books_action(self):
        response = self.client.post(
            reverse("book-status", args=[self.book.pk]),
            {"status": Book.ReadingStatus.CURRENTLY_READING},
        )

        self.book.refresh_from_db()
        self.assertRedirects(response, reverse("book-list"))
        self.assertEqual(self.book.status, Book.ReadingStatus.CURRENTLY_READING)

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


class ReadingDashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.active_book = Book.objects.create(
            owner=self.user,
            title="Active Book",
            author="A Reader",
            status=Book.ReadingStatus.CURRENTLY_READING,
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


class BookSearchAndFilterAcceptanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.dune = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
            status=Book.ReadingStatus.CURRENTLY_READING,
        )
        self.left_hand = Book.objects.create(
            owner=self.user,
            title="The Left Hand of Darkness",
            author="Ursula K. Le Guin",
            status=Book.ReadingStatus.WANT_TO_READ,
        )
        self.paused_book = Book.objects.create(
            owner=self.user,
            title="A Wizard of Earthsea",
            author="Ursula K. Le Guin",
            status=Book.ReadingStatus.PAUSED,
        )
        self.completed_book = Book.objects.create(
            owner=self.user,
            title="Beloved",
            author="Toni Morrison",
            status=Book.ReadingStatus.COMPLETED,
        )
        self.private_book = Book.objects.create(
            owner=self.other_user,
            title="Private Dune Notes",
            author="Frank Herbert",
            status=Book.ReadingStatus.CURRENTLY_READING,
        )
        self.client.force_login(self.user)

    def test_search_matches_title_case_insensitively(self):
        response = self.client.get(reverse("book-list"), {"q": "dUnE"})

        self.assertQuerySetEqual(response.context["books"], [self.dune])

    def test_search_matches_author_case_insensitively(self):
        response = self.client.get(reverse("book-list"), {"q": "ursula k. le guin"})

        self.assertQuerySetEqual(
            response.context["books"],
            [self.paused_book, self.left_hand],
            ordered=False,
        )

    def test_every_defined_status_can_filter_results(self):
        expected_books = {
            Book.ReadingStatus.WANT_TO_READ: self.left_hand,
            Book.ReadingStatus.CURRENTLY_READING: self.dune,
            Book.ReadingStatus.PAUSED: self.paused_book,
            Book.ReadingStatus.COMPLETED: self.completed_book,
        }

        for status, expected_book in expected_books.items():
            with self.subTest(status=status):
                response = self.client.get(reverse("book-list"), {"status": status})
                self.assertQuerySetEqual(response.context["books"], [expected_book])

    def test_search_and_status_filters_can_be_combined(self):
        response = self.client.get(
            reverse("book-list"),
            {"q": "ursula", "status": Book.ReadingStatus.PAUSED},
        )

        self.assertQuerySetEqual(response.context["books"], [self.paused_book])

    def test_filtered_results_remain_owner_scoped(self):
        response = self.client.get(reverse("book-list"), {"q": "dune"})

        self.assertQuerySetEqual(response.context["books"], [self.dune])

    def test_clearing_filters_restores_full_personal_list(self):
        response = self.client.get(reverse("book-list"), {"q": "", "status": ""})

        self.assertQuerySetEqual(
            response.context["books"],
            [self.completed_book, self.paused_book, self.left_hand, self.dune],
            ordered=False,
        )

    def test_unknown_status_is_ignored_safely(self):
        response = self.client.get(reverse("book-list"), {"status": "abandoned"})

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["books"],
            [self.completed_book, self.paused_book, self.left_hand, self.dune],
            ordered=False,
        )

    def test_page_displays_search_status_and_clear_controls(self):
        response = self.client.get(
            reverse("book-list"),
            {"q": "dune", "status": Book.ReadingStatus.CURRENTLY_READING},
        )

        self.assertContains(response, 'name="q"')
        self.assertContains(response, 'value="dune"')
        self.assertContains(response, 'name="status"')
        self.assertContains(response, "Currently Reading")
        self.assertContains(response, 'href="{}"'.format(reverse("book-list")))

    def test_personal_shelf_is_paginated_and_preserves_filters(self):
        for number in range(25):
            Book.objects.create(
                owner=self.user,
                title=f"Extra book {number:02d}",
                author="Demo Author",
                status=Book.ReadingStatus.WANT_TO_READ,
            )

        response = self.client.get(
            reverse("book-list"),
            {"status": Book.ReadingStatus.WANT_TO_READ},
        )

        self.assertTrue(response.context["is_paginated"])
        self.assertContains(response, "Next page")
        self.assertContains(response, "status=want_to_read&amp;page=2")
