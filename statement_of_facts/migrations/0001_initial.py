# Generated by Django 4.2.13 on 2024-08-29 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0004_case_agency'),
        ('employee', '0004_employee_applicant_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatementOfFacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_text', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('finalized', 'Finalized')], max_length=50)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statements_of_facts', to='cases.case')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statements_of_facts', to='employee.employee')),
            ],
        ),
    ]
