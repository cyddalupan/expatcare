# Generated by Django 4.2.13 on 2024-08-18 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("fra", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fra",
            name="agency",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fras",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]