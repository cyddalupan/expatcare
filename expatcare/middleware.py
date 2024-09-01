from django.utils.deprecation import MiddlewareMixin

class CustomAdminMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if request.path.startswith('/admin/'):
            response.context_data['custom_message'] = "Good night world"
        return response
