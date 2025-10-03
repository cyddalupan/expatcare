import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User, Group
from employee.models import Employee
from cases.models import Case, CaseComment
from chats.models import Chat
from support.models import ChatSupport
from fra.models import FRA
from statement_of_facts.models import StatementOfFacts

class Command(BaseCommand):
    help = 'Populates the database with dummy data, avoiding default Django tables.'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get or create groups
        agency_group, _ = Group.objects.get_or_create(name='Agency')

        # Get agency users
        agencies = list(User.objects.filter(groups=agency_group))

        if not agencies:
            self.stdout.write(self.style.WARNING('No agency users found. Skipping population of data that depends on agency users.'))
            return

        # Create employees
        for _ in range(20):
            Employee.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                passport_number=fake.unique.ssn(),
                date_of_birth=fake.date_of_birth(),
                address=fake.address(),
                phone_number=f'+{random.randint(1000000000, 9999999999)}',
                email=fake.email(),
                country=fake.country_code(),
                agency=random.choice(agencies),
                emergency_contact_name=fake.name(),
                emergency_contact_phone=f'+{random.randint(1000000000, 9999999999)}'
            )

        # Create cases
        employees = Employee.objects.all()
        for employee in employees:
            for _ in range(random.randint(1, 5)):
                Case.objects.create(
                    employee=employee,
                    category=fake.word(),
                    report=fake.text(),
                    agency=employee.agency
                )

        # Create case comments
        cases = Case.objects.all()
        for case in cases:
            for _ in range(random.randint(1, 10)):
                CaseComment.objects.create(
                    case=case,
                    author=case.agency,
                    text=fake.text()
                )

        # Create chats
        employees = Employee.objects.all()
        for _ in range(50):
            Chat.objects.create(
                employee=random.choice(employees),
                agency=random.choice(agencies),
                message=fake.text(),
                sender=random.choice(['User', 'AI'])
            )
        
        # Create ChatSupport
        employees = Employee.objects.all()
        for employee in employees:
            if random.choice([True, False]):
                ChatSupport.objects.create(
                    employee=employee,
                    is_open=random.choice([True, False]),
                    last_message=fake.text()
                )

        # Create FRAs
        for agency in agencies:
            for _ in range(random.randint(1, 3)):
                FRA.objects.create(
                    name=fake.company(),
                    contact=fake.name(),
                    address=fake.address(),
                    country=fake.country_code(),
                    agency=agency
                )

        # Create Statements of Facts
        employees = Employee.objects.all()
        for employee in employees:
            for _ in range(random.randint(1, 2)):
                StatementOfFacts.objects.create(
                    employee=employee,
                    generated_text=fake.text(),
                    emotion=fake.word(),
                    status=random.choice(['draft', 'finalized']),
                    consistency_analysis=fake.text(),
                    ai_reference_link=fake.url()
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))
