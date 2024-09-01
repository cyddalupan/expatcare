from django.shortcuts import render
from django.db.models import Count
from employee.models import Employee

def custom_dashboard_data(request):
    # Query active employees grouped by country
    active_cases_by_country = Employee.objects.filter(main_status='active').values('country').annotate(total=Count('id')).order_by('-total')

    context = {
        'active_cases_by_country': active_cases_by_country,
    }
    return render(request, 'admin/custom_dashboard.html', context)