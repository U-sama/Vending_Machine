# Generated by Django 5.0.1 on 2024-02-05 23:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("API", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="sellerId",
            new_name="seller",
        ),
    ]
