# Generated by Django 5.1.4 on 2025-01-21 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("link", "0003_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ("name",)},
        ),
        migrations.AlterModelOptions(
            name="link",
            options={"ordering": ("-created_at",)},
        ),
    ]
