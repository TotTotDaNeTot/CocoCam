# Generated by Django 5.1.4 on 2025-02-10 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_user_plan"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="plan",
        ),
    ]
