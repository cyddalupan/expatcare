# expatcare/middleware.py

from django.utils.deprecation import MiddlewareMixin
from employee.models import Employee
from django.db.models import Count, Q
import random
from django_countries import countries
from django.utils import timezone
import calendar

class CustomAdminMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if request.path.startswith('/admin/'):
            # Define possible Bootstrap background color classes
            colors = ['bg-primary', 'bg-success', 'bg-info', 'bg-warning', 'bg-danger']

            # Query employees grouped by status and country, and organize them by status
            status_groups = {}
            statuses = ['active', 'with_hearing', 'with_complain', 'no_communication', 'arrive', 'blacklist']

            for status in statuses:
                cases_by_status = Employee.objects.filter(main_status=status).values('country').annotate(total=Count('id')).order_by('-total')
                if cases_by_status:
                    status_groups[status] = []
                    for case in cases_by_status:
                        case['color'] = random.choice(colors)
                        case['country_name'] = countries.name(case['country'])
                        status_groups[status].append(case)

            # Summary statistics grouped by month, ignoring null or blank deployment dates
            current_year = timezone.now().year
            summary_data = Employee.objects.filter(
                date_deployment__year=current_year
            ).exclude(
                date_deployment__isnull=True
            ).values(
                'date_deployment__month'
            ).annotate(
                total_deployed=Count('id'),
                complaints=Count('id', filter=Q(main_status='with_complain')),
                hearings=Count('id', filter=Q(main_status='with_hearing')),
                no_communication=Count('id', filter=Q(main_status='no_communication')),
                arrived=Count('id', filter=Q(main_status='arrive'))
            ).order_by('date_deployment__month')

            for data in summary_data:
                data['month_name'] = calendar.month_name[data['date_deployment__month']]

            # Add the custom data to the context
            response.context_data['status_groups'] = status_groups
            response.context_data['summary_data'] = summary_data
        return response
