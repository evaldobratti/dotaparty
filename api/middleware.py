from core import models
from django.db.models import F


class VisitMiddleware(object):
    def process_request(self, request):
        visit, _ = models.Visit.objects.get_or_create(host=self.get_ip(request)[:400],
                                                      requested=request.get_full_path()[:400])
        visit.count = F('count') + 1
        visit.save()

    def get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        else:
            return request.META.get('REMOTE_ADDR')