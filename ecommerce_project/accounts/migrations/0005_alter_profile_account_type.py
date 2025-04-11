# Generated by Django 5.1.7 on 2025-03-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_profile_account_type_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="account_type",
            field=models.CharField(
                choices=[("vendor", "Vendor"), ("buyer", "Buyer")],
                default="vendor",
                max_length=50,
            ),
        ),
    ]
