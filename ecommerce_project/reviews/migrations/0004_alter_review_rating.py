# Generated by Django 5.1.7 on 2025-03-23 15:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0003_alter_review_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ]
            ),
        ),
    ]
