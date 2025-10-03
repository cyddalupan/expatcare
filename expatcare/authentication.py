from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from employee.models import Employee

class EmployeeTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            employee = Employee.objects.get(token=key)
        except Employee.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        return (employee, None)
