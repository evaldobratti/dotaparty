from django.views.generic import View
from django.http import JsonResponse
from api.serializers import account_serializer
from core import utils
from core import models
import time


def seconds_since_epoch(date):
    return time.mktime(date.timetuple())


class ReportsView(View):

    def dispatch(self, request, account_id, *args, **kwargs):
        self.required_account = utils.get_account(account_id)
        self.logged_account = request.user.account if request.user.is_authenticated() else None

        self.own_profile = self.required_account == self.logged_account
        self.elements_per_page = 5
        self.page = 1

        return super(ReportsView, self).dispatch(request, *args, **kwargs)

    def serialize(self, query, total):
        from django.core.paginator import Paginator
        paginator = Paginator(query, self.elements_per_page)
        page = paginator.page(self.page)

        return {
            'reports': map(self.report_serializer, page),
            'current_page': page.number,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'total': total
        }

    def report_serializer(self, report):
        serialized = {
            'created': seconds_since_epoch(report.date_created),
            'reason': report.reason,
            'due_to_match_id': report.due_to_match.match_id
        }

        if self.show_creator():
            serialized['creator'] = account_serializer(report.creator)

            serialized['reported'] = account_serializer(report.reported)

        return serialized


class ReportsReceived(ReportsView):

    def get(self, request):
        if self.own_profile:
            reports_received = self.required_account.reports_received.all().order_by('-date_created')
        else:
            reports_received = self.required_account.reports_received.filter(creator=self.logged_account).order_by('-date_created')

        return JsonResponse(self.serialize(reports_received, len(self.required_account.reports_received.all())))

    def show_creator(self):
        return not self.own_profile


class ReportsCreated(ReportsView):

    def get(self, request):
        others = request.GET.get('others', '')

        if self.own_profile:
            reports_created = self.required_account.reports_created.all()
            if others:
                reports_created = reports_created.filter(reported__account_id__in=map(int, others.split(',')))
            reports_created = reports_created.order_by('-date_created')
        else:
            reports_created = []

        return JsonResponse(self.serialize(reports_created, len(self.required_account.reports_created.all())))

    def show_creator(self):
        return self.own_profile
