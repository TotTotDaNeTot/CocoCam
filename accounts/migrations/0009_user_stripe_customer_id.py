# Generated by Django 5.1.4 on 2025-02-11 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_user_plan"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="stripe_customer_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
