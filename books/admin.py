from django.contrib import admin

from .models import Book, CatalogBook, Category, Forum, ForumPost, ReadingNote


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "source", "created_by", "created_at")
    list_filter = ("source",)
    search_fields = ("name",)


@admin.register(CatalogBook)
class CatalogBookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn_13", "publisher", "updated_at")
    search_fields = ("title", "author", "isbn_10", "isbn_13")
    filter_horizontal = ("categories",)


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


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "book", "created_by", "created_at")
    search_fields = ("title", "description", "book__title")
    list_select_related = ("book", "created_by")


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ("title", "forum", "author", "updated_at")
    search_fields = ("title", "content", "author__username", "forum__title")
    list_select_related = ("forum", "author")
