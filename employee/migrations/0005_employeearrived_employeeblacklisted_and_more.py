# Generated by Django 4.2.13 on 2024-09-01 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_employee_applicant_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeArrived',
            fields=[
            ],
            options={
                'verbose_name': 'Employee Arrived',
                'verbose_name_plural': 'Employees Arrived',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('employee.employee',),
        ),
        migrations.CreateModel(
            name='EmployeeBlacklisted',
            fields=[
            ],
            options={
                'verbose_name': 'Blacklisted Employee',
                'verbose_name_plural': 'Blacklisted Employees',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('employee.employee',),
        ),
        migrations.CreateModel(
            name='EmployeeClosedCases',
            fields=[
            ],
            options={
                'verbose_name': 'Employee with Closed Case',
                'verbose_name_plural': 'Employees with Closed Cases',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('employee.employee',),
        ),
        migrations.CreateModel(
            name='EmployeeNoCommunication',
            fields=[
            ],
            options={
                'verbose_name': 'Employee with No Communication',
                'verbose_name_plural': 'Employees with No Communication',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('employee.employee',),
        ),
        migrations.CreateModel(
            name='EmployeeWithComplaints',
            fields=[
            ],
            options={
                'verbose_name': 'Employee with Complaint',
                'verbose_name_plural': 'Employees with Complaints',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('employee.employee',),
        ),
        migrations.CreateModel(
            name='EmployeeWithHearings',
            fields=[
            ],
            options={
                'verbose_name': 'Employee with Hearing',
                'verbose_name_plural': 'Employees with Hearings',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('employee.employee',),
        ),
    ]
