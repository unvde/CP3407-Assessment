from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Book, ReadingNote


class ReadingNoteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
        )

    def test_note_belongs_to_a_book_and_retains_content(self):
        note = ReadingNote.objects.create(
            book=self.book,
            content="Fear is the mind-killer.",
        )

        self.assertEqual(note.book, self.book)
        self.assertEqual(note.content, "Fear is the mind-killer.")
        self.assertQuerySetEqual(self.book.notes.all(), [note])

    def test_blank_note_content_is_rejected(self):
        note = ReadingNote(book=self.book, content="   ")

        with self.assertRaises(ValidationError):
            note.full_clean()

    def test_deleting_book_cascades_to_notes(self):
        note = ReadingNote.objects.create(book=self.book, content="Private note")

        self.book.delete()

        self.assertFalse(ReadingNote.objects.filter(pk=note.pk).exists())


class PrivateReadingNoteAcceptanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.book = Book.objects.create(
            owner=self.user,
            title="Dune",
            author="Frank Herbert",
        )
        self.other_book = Book.objects.create(
            owner=self.other_user,
            title="Beloved",
            author="Toni Morrison",
        )
        self.note = ReadingNote.objects.create(
            book=self.book,
            content="Original private observation",
        )
        self.other_note = ReadingNote.objects.create(
            book=self.other_book,
            content="Another reader's private note",
        )
        self.client.force_login(self.user)

    def test_reader_can_create_note_on_owned_book(self):
        response = self.client.post(
            reverse("note-add", args=[self.book.pk]),
            {"content": "A new observation"},
        )

        created = ReadingNote.objects.get(content="A new observation")
        self.assertEqual(created.book, self.book)
        self.assertRedirects(response, self.book.get_absolute_url())

    def test_blank_note_is_rejected_by_create_workflow(self):
        response = self.client.post(
            reverse("note-add", args=[self.book.pk]),
            {"content": "   "},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Note content cannot be blank.")
        self.assertEqual(self.book.notes.count(), 1)

    def test_reader_can_edit_owned_note(self):
        response = self.client.post(
            reverse("note-edit", args=[self.note.pk]),
            {"content": "Updated private observation"},
        )

        self.note.refresh_from_db()
        self.assertEqual(self.note.content, "Updated private observation")
        self.assertRedirects(response, self.book.get_absolute_url())

    def test_reader_can_delete_owned_note(self):
        response = self.client.post(reverse("note-delete", args=[self.note.pk]))

        self.assertRedirects(response, self.book.get_absolute_url())
        self.assertFalse(ReadingNote.objects.filter(pk=self.note.pk).exists())

    def test_owned_notes_appear_only_on_owned_book_detail(self):
        response = self.client.get(self.book.get_absolute_url())

        self.assertContains(response, self.note.content)
        self.assertNotContains(response, self.other_note.content)

    def test_reader_cannot_create_note_on_another_readers_book(self):
        response = self.client.post(
            reverse("note-add", args=[self.other_book.pk]),
            {"content": "Intrusion"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(ReadingNote.objects.filter(content="Intrusion").exists())

    def test_reader_cannot_edit_another_readers_note(self):
        response = self.client.post(
            reverse("note-edit", args=[self.other_note.pk]),
            {"content": "Changed"},
        )

        self.assertEqual(response.status_code, 404)
        self.other_note.refresh_from_db()
        self.assertEqual(self.other_note.content, "Another reader's private note")

    def test_reader_cannot_delete_another_readers_note(self):
        response = self.client.post(
            reverse("note-delete", args=[self.other_note.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(ReadingNote.objects.filter(pk=self.other_note.pk).exists())

    def test_anonymous_reader_is_redirected_from_create_and_edit(self):
        self.client.logout()
        routes = [
            reverse("note-add", args=[self.book.pk]),
            reverse("note-edit", args=[self.note.pk]),
        ]

        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertRedirects(response, f"{reverse('login')}?next={route}")

    def test_anonymous_reader_is_redirected_from_delete(self):
        self.client.logout()
        route = reverse("note-delete", args=[self.note.pk])

        response = self.client.get(route)

        self.assertRedirects(response, f"{reverse('login')}?next={route}")
