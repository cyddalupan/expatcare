# expatcare/middleware.py

from django.utils.deprecation import MiddlewareMixin
from employee.models import Employee
from django.db.models import Count
import random
from django_countries import countries

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

            # Add the custom data to the context
            response.context_data['status_groups'] = status_groups
        return response
