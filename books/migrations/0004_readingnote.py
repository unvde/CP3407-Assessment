import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_target_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='books.book')),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
                'constraints': [models.CheckConstraint(condition=models.Q(('content', ''), _negated=True), name='reading_note_content_not_empty')],
            },
        ),
    ]
