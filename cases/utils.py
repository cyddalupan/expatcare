from django.shortcuts import get_object_or_404
from employee.models import EmployeeMemory

# TODO: remove this
def save_memory(employee_id, memory_content):
    # Assuming you already have models imported
    employee = get_object_or_404(Employee, pk=employee_id)
    user = get_object_or_404(User, username=added_by)
    
    # Create a new EmployeeMemory entry
    EmployeeMemory.objects.create(
        employee=employee,
        note=memory_content,
    )
    return {"status": "Memory saved successfully"}