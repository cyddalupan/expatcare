# Generated by Django 4.2.13 on 2024-07-21 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='report_status',
            field=models.CharField(choices=[('open', 'Open'), ('investigation', 'Investigation'), ('closed', 'Closed'), ('pending', 'Pending'), ('reopened', 'Reopened')], default='open', max_length=15),
        ),
    ]
