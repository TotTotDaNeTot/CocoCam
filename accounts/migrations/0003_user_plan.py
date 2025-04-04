# Generated by Django 5.1.4 on 2025-01-21 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_plan"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="plan",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="accounts.plan",
            ),
            preserve_default=False,
        ),
    ]
