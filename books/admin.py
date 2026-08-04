from django.contrib import admin

from .models import (
    Book,
    CatalogBook,
    Category,
    Forum,
    ForumPost,
    ForumReply,
    PublicReview,
    RecommendationDismissal,
    ReadingList,
    ReadingNote,
)


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


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "updated_at")
    search_fields = ("content", "author__username", "post__title")
    list_select_related = ("post", "author")


@admin.register(PublicReview)
class PublicReviewAdmin(admin.ModelAdmin):
    list_display = ("catalog_book", "rating", "author", "updated_at")
    list_filter = ("rating",)
    search_fields = ("catalog_book__title", "author__username", "content")
    list_select_related = ("catalog_book", "author")


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_public", "updated_at")
    list_filter = ("is_public",)
    search_fields = ("name", "description", "owner__username")
    filter_horizontal = ("books",)


@admin.register(RecommendationDismissal)
class RecommendationDismissalAdmin(admin.ModelAdmin):
    list_display = ("user", "identifier", "created_at")
    search_fields = ("user__username", "identifier")
    list_select_related = ("user",)
