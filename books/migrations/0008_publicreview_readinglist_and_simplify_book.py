import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0007_forumreply"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PublicReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("content", models.TextField(max_length=3000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("author", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="public_book_reviews", to=settings.AUTH_USER_MODEL)),
                ("catalog_book", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="books.catalogbook")),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.CreateModel(
            name="ReadingList",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True, max_length=500)),
                ("is_public", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("books", models.ManyToManyField(blank=True, related_name="reading_lists", to="books.catalogbook")),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reading_lists", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at", "name"]},
        ),
        migrations.AddConstraint(
            model_name="publicreview",
            constraint=models.UniqueConstraint(fields=("catalog_book", "author"), name="one_public_review_per_book_and_author"),
        ),
        migrations.AddConstraint(
            model_name="readinglist",
            constraint=models.UniqueConstraint(fields=("owner", "name"), name="unique_reading_list_name_per_owner"),
        ),
        migrations.RemoveField(model_name="book", name="completion_date"),
        migrations.RemoveField(model_name="book", name="current_page"),
        migrations.RemoveField(model_name="book", name="rating"),
        migrations.RemoveField(model_name="book", name="reflection"),
        migrations.RemoveField(model_name="book", name="target_date"),
        migrations.RemoveField(model_name="book", name="total_pages"),
    ]
