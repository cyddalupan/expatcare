# Generated by Django 4.2.13 on 2024-08-18 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fra", "0001_initial"),
        ("employee", "0002_alter_employee_options_employee_agency"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="fra",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="fra.fra",
            ),
        ),
    ]
