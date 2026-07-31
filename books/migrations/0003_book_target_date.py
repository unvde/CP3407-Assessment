from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_book_current_page"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="target_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
