# Generated by Django 4.2.13 on 2024-08-30 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statement_of_facts', '0004_statementoffacts_ai_reference_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='statementoffacts',
            name='consistency_analysis',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
