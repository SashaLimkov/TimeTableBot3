# Generated by Django 4.2.7 on 2023-12-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="telegramuser",
            name="notifications",
            field=models.BooleanField(
                default=False, verbose_name="Уведомления включены?"
            ),
        ),
    ]
