# Generated by Django 4.2.13 on 2024-09-03 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0004_case_agency'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]