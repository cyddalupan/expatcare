# Generated by Django 4.2.13 on 2024-09-27 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0006_employeememory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_message', models.TextField()),
                ('is_open', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='employee.employee')),
            ],
        ),
    ]
