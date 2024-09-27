import json
from django.shortcuts import get_object_or_404
from cases.models import Case
from employee.models import Employee, EmployeeMemory


def get_category(category, welcome_message):
    return "systeminfo$:$" + (category or "") + "$:$" + (welcome_message or "")
    
def save_memory(employee_id, memory_content):
    employee = get_object_or_404(Employee, pk=employee_id)
    
    # Create a new EmployeeMemory entry
    EmployeeMemory.objects.create(
        employee=employee,
        note=memory_content,
    )
    return {"status": "Memory saved successfully"}

def get_report(employee_id):
    # Retrieve the Employee instance
    employee = Employee.objects.get(id=employee_id)

    # Retrieve all cases related to the employee
    cases = Case.objects.filter(employee=employee)

    # Check if any cases are found
    if not cases.exists():
        return "systeminfo$:$chat$:$Wala ka pang nagagawang reklamo, gusto mo ba mag reklamo?."

    # Format the message
    message = f"systeminfo$:$chat$:$Eto ang lagay ng iyong report {employee.first_name} {employee.last_name}:<br/>"
    for case in cases:
        message += f"- {case.category}: {case.get_report_status_display()}<br/>"
    return message

def get_param_names(category):
    param_names = []
    if category.param_one_name and category.param_one_name.strip():
        param_names.append(category.param_one_name)
    if category.param_two_name and category.param_two_name.strip():
        param_names.append(category.param_two_name)
    if category.param_three_name and category.param_three_name.strip():
        param_names.append(category.param_three_name)
    if category.param_four_name and category.param_four_name.strip():
        param_names.append(category.param_four_name)
    param_names.append("summary")
    return param_names

def log_case(employee_id, category, arguments):
    arguments_dict = json.loads(arguments)
    readable_format = "\n".join([f"{key.capitalize()}: {value}" for key, value in arguments_dict.items()])

    try:
        employee = Employee.objects.get(id=employee_id)
        
        try:
            case = Case.objects.get(employee=employee, category=category)
            case.report = readable_format
            case.save()
        except Case.DoesNotExist:
            case = Case.objects.create(
                employee=employee,
                category=category,
                report=readable_format,
                agency=employee.agency
            )

        # Check if all required parameters are present
        all_expected_params = get_param_names(category)
        provided_params = arguments_dict.keys()

        if set(all_expected_params) <= set(provided_params):
            # All required parameters are present
            return "systeminfo$:$chat$:$" + (category.closing_message or "")
        else:
            # Not all required parameters are present
            return None

    except Employee.DoesNotExist:
        return "Employee not found"
    except Exception as e:
        return str(e)
  
def get_properties(category):
    properties = {}
    if category.param_one_name and category.param_one_name.strip():
        properties[category.param_one_name] = {
            "type": "string",
            "description": category.param_one_desc,
        }
        if category.param_one_enum and category.param_one_enum.strip():
            properties[category.param_one_name]["enum"] = category.param_one_enum.split(',')
    
    if category.param_two_name and category.param_two_name.strip():
        properties[category.param_two_name] = {
            "type": "string",
            "description": category.param_two_desc,
        }
        if category.param_two_enum and category.param_two_enum.strip():
            properties[category.param_two_name]["enum"] = category.param_two_enum.split(',')
    
    if category.param_three_name and category.param_three_name.strip():
        properties[category.param_three_name] = {
            "type": "string",
            "description": category.param_three_desc,
        }
        if category.param_three_enum and category.param_three_enum.strip():
            properties[category.param_three_name]["enum"] = category.param_three_enum.split(',')
    
    if category.param_four_name and category.param_four_name.strip():
        properties[category.param_four_name] = {
            "type": "string",
            "description": category.param_four_desc,
        }
        if category.param_four_enum and category.param_four_enum.strip():
            properties[category.param_four_name]["enum"] = category.param_four_enum.split(',')
    
    properties["summary"] = {
        "type": "string",
        "description": "The summary of the problem. Compile and make it look like a report.",
    }
    return properties