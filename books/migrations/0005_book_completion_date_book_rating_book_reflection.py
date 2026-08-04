import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_readingnote'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='book',
            name='reflection',
            field=models.TextField(blank=True, max_length=1000, validators=[django.core.validators.MaxLengthValidator(1000)]),
        ),
    ]
