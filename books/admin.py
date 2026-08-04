from django.contrib import admin

from .models import Book, ReadingNote


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "owner",
        "status",
        "rating",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = ("title", "author", "owner__username")


@admin.register(ReadingNote)
class ReadingNoteAdmin(admin.ModelAdmin):
    list_display = ("book", "updated_at")
    search_fields = ("book__title", "book__author", "content")
    list_select_related = ("book",)
