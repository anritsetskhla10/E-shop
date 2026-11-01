from django.conf import settings
from django.shortcuts import render


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_maintenance = getattr(settings, 'MAINTENANCE_MODE', False)

        # თუ ჩართულია ტექნიკური რეჟიმი და მოთხოვნა არ მიდის /admin/-ზე
        if is_maintenance and not request.path.startswith('/admin/'):
            return render(request, 'shop/maintenance.html', status=503)

        return self.get_response(request)