from core import models
from django.db.models import F


class VisitMiddleware(object):
    def process_request(self, request):
        models.Visit.objects.update_or_create(host=self.get_ip(request), requested=request.get_full_path(), defaults={
            'count': F('count') + 1
        })

    def get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip