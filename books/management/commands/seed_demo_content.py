from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from books.models import (
    Book,
    CatalogBook,
    Category,
    Forum,
    ForumPost,
    ForumReply,
    PublicReview,
    ReadingList,
    ReadingNote,
)


BOOKS = [
    ("Dune", "Frank Herbert", "9780441172719", "OL893415W", 1965, ("Science Fiction", "Classics", "Adventure")),
    ("The Left Hand of Darkness", "Ursula K. Le Guin", "9780441478125", "OL27258W", 1969, ("Science Fiction", "Classics")),
    ("Foundation", "Isaac Asimov", "9780553293357", "OL46125W", 1951, ("Science Fiction", "Classics")),
    ("Nineteen Eighty-Four", "George Orwell", "9780451524935", "OL1168083W", 1949, ("Dystopian", "Classics", "Science Fiction")),
    ("The Hobbit", "J. R. R. Tolkien", "9780547928227", "OL262758W", 1937, ("Fantasy", "Classics", "Adventure")),
    ("Pride and Prejudice", "Jane Austen", "9780141439518", "OL66554W", 1813, ("Romance", "Classics")),
    ("Jane Eyre", "Charlotte Brontë", "9780141441146", "OL103123W", 1847, ("Romance", "Classics")),
    ("Murder on the Orient Express", "Agatha Christie", "9780062693662", "OL15573W", 1934, ("Mystery", "Classics")),
    ("Project Hail Mary", "Andy Weir", "9780593135204", "OL20986705W", 2021, ("Science Fiction", "Adventure")),
    ("The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", "9781501161933", "OL17929490W", 2017, ("Romance", "Historical Fiction")),
]

READERS = [
    ("demo_alex", "Alex", "Morgan"),
    ("demo_maya", "Maya", "Chen"),
    ("demo_noah", "Noah", "Williams"),
    ("demo_lina", "Lina", "Patel"),
]


class Command(BaseCommand):
    help = "Create an idempotent set of realistic demo community activity."

    def add_arguments(self, parser):
        parser.add_argument("--reader-password", required=True)
        parser.add_argument("--admin-password", required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        reader_password = options["reader_password"]
        admin_password = options["admin_password"]
        users = {}
        for username, first_name, last_name in READERS:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={"email": f"{username}@readingcompass.demo"},
            )
            user.first_name = first_name
            user.last_name = last_name
            user.email = f"{username}@readingcompass.demo"
            user.is_active = True
            user.set_password(reader_password)
            user.save()
            users[username] = user

        admin, _ = User.objects.get_or_create(
            username="reading_admin",
            defaults={"email": "admin@readingcompass.demo"},
        )
        admin.first_name = "Reading"
        admin.last_name = "Administrator"
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password(admin_password)
        admin.save()

        categories = {}
        for names in (book[5] for book in BOOKS):
            for name in names:
                category = Category.objects.filter(name__iexact=name).first()
                if not category:
                    category = Category.objects.create(
                        name=name,
                        source=Category.Source.API,
                        created_by=admin,
                    )
                categories[name] = category

        catalog = {}
        for title, author, isbn, work_key, year, category_names in BOOKS:
            catalog_book = CatalogBook.objects.filter(
                open_library_key=work_key
            ).first() or CatalogBook.objects.filter(isbn_13=isbn).first()
            if not catalog_book:
                catalog_book = CatalogBook(added_by=admin)
            catalog_book.title = title
            catalog_book.author = author
            catalog_book.isbn_13 = isbn
            catalog_book.open_library_key = work_key
            catalog_book.cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
            catalog_book.published_year = year
            catalog_book.save()
            catalog_book.categories.set(
                [categories[name] for name in category_names]
            )
            catalog[title] = catalog_book

        shelves = {
            "demo_alex": [("Dune", Book.ReadingStatus.COMPLETED), ("Project Hail Mary", Book.ReadingStatus.CURRENTLY_READING), ("Foundation", Book.ReadingStatus.WANT_TO_READ), ("The Hobbit", Book.ReadingStatus.PAUSED)],
            "demo_maya": [("The Left Hand of Darkness", Book.ReadingStatus.COMPLETED), ("Jane Eyre", Book.ReadingStatus.CURRENTLY_READING), ("Pride and Prejudice", Book.ReadingStatus.COMPLETED)],
            "demo_noah": [("Murder on the Orient Express", Book.ReadingStatus.COMPLETED), ("Nineteen Eighty-Four", Book.ReadingStatus.CURRENTLY_READING), ("Dune", Book.ReadingStatus.WANT_TO_READ)],
            "demo_lina": [("The Seven Husbands of Evelyn Hugo", Book.ReadingStatus.COMPLETED), ("The Hobbit", Book.ReadingStatus.CURRENTLY_READING), ("Project Hail Mary", Book.ReadingStatus.WANT_TO_READ)],
        }
        shelf_entries = {}
        for username, entries in shelves.items():
            for title, status in entries:
                entry, _ = Book.objects.update_or_create(
                    owner=users[username],
                    catalog_book=catalog[title],
                    defaults={"title": title, "author": catalog[title].author, "status": status},
                )
                shelf_entries[(username, title)] = entry

        notes = [
            ("demo_alex", "Project Hail Mary", "The science puzzles make the pacing work; note the shift from isolation to cooperation."),
            ("demo_maya", "Jane Eyre", "The tension between independence and belonging is stronger than I remembered."),
            ("demo_noah", "Nineteen Eighty-Four", "Track how language changes what the characters are able to imagine."),
            ("demo_lina", "The Hobbit", "A warm reread. Bilbo's confidence grows in very small, believable steps."),
        ]
        for username, title, content in notes:
            ReadingNote.objects.update_or_create(
                book=shelf_entries[(username, title)], defaults={"content": content}
            )

        reviews = [
            ("demo_alex", "Dune", 5, "Dense at first, but the ecology, politics and sense of scale reward patience."),
            ("demo_alex", "Project Hail Mary", 4, "Fast, optimistic science fiction with a friendship at its centre."),
            ("demo_maya", "The Left Hand of Darkness", 5, "Quietly radical and beautifully observed. The journey across the ice stayed with me."),
            ("demo_maya", "Pride and Prejudice", 4, "Sharp, funny, and much warmer than its reputation suggests."),
            ("demo_noah", "Murder on the Orient Express", 4, "A compact mystery whose ending still invites an argument."),
            ("demo_noah", "Nineteen Eighty-Four", 5, "Bleak but precise about how power reshapes language and memory."),
            ("demo_lina", "The Seven Husbands of Evelyn Hugo", 4, "Compulsive storytelling with more moral complexity than I expected."),
            ("demo_lina", "The Hobbit", 5, "Comforting, adventurous, and still one of the best invitations into fantasy."),
        ]
        for username, title, rating, content in reviews:
            PublicReview.objects.update_or_create(
                catalog_book=catalog[title],
                author=users[username],
                defaults={"rating": rating, "content": content},
            )

        list_specs = [
            ("demo_alex", "Big ideas in space", "Science fiction where the ideas matter as much as the action.", True, ["Dune", "Foundation", "Project Hail Mary", "The Left Hand of Darkness"]),
            ("demo_maya", "Classics that feel alive", "Older novels that still start conversations.", True, ["Pride and Prejudice", "Jane Eyre", "The Left Hand of Darkness"]),
            ("demo_noah", "Uneasy worlds", "Mysteries and dystopias for a darker weekend.", True, ["Nineteen Eighty-Four", "Murder on the Orient Express", "Dune"]),
            ("demo_lina", "Comfort reads", "Books I would happily revisit on a quiet afternoon.", True, ["The Hobbit", "Pride and Prejudice", "The Seven Husbands of Evelyn Hugo"]),
            ("demo_alex", "Maybe next month", "A private shortlist.", False, ["Jane Eyre", "The Hobbit"]),
        ]
        for username, name, description, is_public, titles in list_specs:
            reading_list, _ = ReadingList.objects.update_or_create(
                owner=users[username],
                name=name,
                defaults={"description": description, "is_public": is_public},
            )
            reading_list.books.set([catalog[title] for title in titles])

        forum, _ = Forum.objects.update_or_create(
            book=catalog["Dune"],
            defaults={
                "title": "Dune: ecology, power and prophecy",
                "description": "Discuss the novel's ideas, characters and adaptations.",
                "created_by": users["demo_alex"],
            },
        )
        post_one, _ = ForumPost.objects.update_or_create(
            forum=forum,
            author=users["demo_alex"],
            title="Is Paul a hero, or a warning?",
            defaults={"content": "The book gives Paul heroic abilities but keeps showing the danger of people turning him into a symbol. How did you read him?"},
        )
        ForumReply.objects.get_or_create(
            post=post_one,
            author=users["demo_maya"],
            content="A warning for me. His awareness of the consequences makes the choices more tragic, not less responsible.",
        )
        ForumReply.objects.get_or_create(
            post=post_one,
            author=users["demo_noah"],
            content="I think the first book deliberately lets the surface-level hero story remain tempting.",
        )
        ForumPost.objects.update_or_create(
            forum=forum,
            author=users["demo_lina"],
            title="The small details that make Arrakis convincing",
            defaults={"content": "Water discipline appears in clothing, manners, grief and politics. Which detail made the world feel real to you?"},
        )

        now = timezone.now()
        for index, review in enumerate(PublicReview.objects.filter(author__username__startswith="demo_")):
            PublicReview.objects.filter(pk=review.pk).update(
                created_at=now - timedelta(days=index + 1),
                updated_at=now - timedelta(days=index),
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo activity ready: 4 readers, 1 administrator, 10 books, shelves, lists, reviews and forum activity."
            )
        )
