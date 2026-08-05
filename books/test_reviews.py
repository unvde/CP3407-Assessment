from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import CatalogBook, PublicReview


class PublicReviewTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username="reader", password="pass")
        self.other = User.objects.create_user(username="other", password="pass")
        self.staff = User.objects.create_user(
            username="moderator", password="pass", is_staff=True
        )
        self.book = CatalogBook.objects.create(title="Dune", author="Frank Herbert")

    def test_rating_must_be_between_one_and_five(self):
        for rating in (0, 6):
            review = PublicReview(
                catalog_book=self.book,
                author=self.reader,
                rating=rating,
                content="A review.",
            )
            with self.subTest(rating=rating), self.assertRaises(ValidationError):
                review.full_clean()

    def test_one_review_per_reader_and_book(self):
        PublicReview.objects.create(
            catalog_book=self.book,
            author=self.reader,
            rating=5,
            content="Excellent.",
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            PublicReview.objects.create(
                catalog_book=self.book,
                author=self.reader,
                rating=4,
                content="Duplicate.",
            )

    def test_reader_can_publish_and_update_public_review(self):
        self.client.force_login(self.reader)
        route = reverse("public-review-upsert", args=[self.book.pk])
        response = self.client.post(
            route,
            {"rating": 5, "content": "A landmark science-fiction novel."},
        )
        review = PublicReview.objects.get(author=self.reader, catalog_book=self.book)
        self.assertRedirects(response, review.get_absolute_url())

        response = self.client.post(
            route,
            {"rating": 4, "content": "Still excellent on a reread."},
        )
        review.refresh_from_db()
        self.assertRedirects(response, review.get_absolute_url())
        self.assertEqual(review.rating, 4)
        self.assertEqual(PublicReview.objects.count(), 1)

    def test_review_and_average_are_public(self):
        PublicReview.objects.create(
            catalog_book=self.book,
            author=self.reader,
            rating=5,
            content="Public recommendation.",
        )
        PublicReview.objects.create(
            catalog_book=self.book,
            author=self.other,
            rating=3,
            content="Mixed feelings.",
        )

        response = self.client.get(self.book.get_absolute_url())

        self.assertContains(response, "Public recommendation.")
        self.assertContains(response, "4.0 / 5")

    def test_public_reviews_are_paginated(self):
        for number in range(13):
            reviewer = User.objects.create_user(
                username=f"reviewer-{number:02d}", password="pass"
            )
            PublicReview.objects.create(
                catalog_book=self.book,
                author=reviewer,
                rating=4,
                content=f"Review number {number:02d}.",
            )

        first_page = self.client.get(self.book.get_absolute_url())
        second_page = self.client.get(
            self.book.get_absolute_url(), {"review_page": 2}
        )

        self.assertTrue(first_page.context["reviews_are_paginated"])
        self.assertContains(first_page, "Next reviews")
        self.assertEqual(len(second_page.context["reviews"]), 1)

    def test_reader_cannot_edit_another_review_but_staff_can_delete_it(self):
        review = PublicReview.objects.create(
            catalog_book=self.book,
            author=self.reader,
            rating=5,
            content="Original review.",
        )
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("public-review-edit", args=[review.pk]),
            {"rating": 1, "content": "Hijacked."},
        )
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.staff)
        response = self.client.post(reverse("public-review-delete", args=[review.pk]))
        self.assertRedirects(response, self.book.get_absolute_url())
        self.assertFalse(PublicReview.objects.filter(pk=review.pk).exists())

    def test_anonymous_reader_is_redirected_from_review_form(self):
        route = reverse("public-review-upsert", args=[self.book.pk])
        self.assertRedirects(
            self.client.get(route),
            f"{reverse('login')}?next={route}",
        )
