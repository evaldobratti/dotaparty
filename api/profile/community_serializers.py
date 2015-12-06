import functools
import time
from core import utils
from api.serializers import account_serializer


def seconds_since_epoch(date):
    return time.mktime(date.timetuple())


def serialize_friend(friend):
    return {
        'account_id': friend.account_id,
        'persona_name': friend.persona_name,
        'url_avatar': friend.url_avatar,
        'qtd': friend.qtd
    }


def report_serializer(report, show_creator_info=True):
    serialized = {
        'created': seconds_since_epoch(report.date_created),
        'reason': report.reason,
        'due_to_match_id': report.due_to_match.match_id
    }

    if show_creator_info:
        serialized['creator'] = account_serializer(report.creator)
        serialized['reported'] = account_serializer(report.reported)

    return serialized


def profile_serializer(account_id, others_accounts_ids, logged_account):
    account = utils.get_account(account_id)
    friends = utils.get_friends_number_matches(account, others_accounts_ids)

    return {
        'account_id': account.account_id,
        'persona_name': account.current_update.persona_name,
        'url_avatar': account.current_update.url_avatar,
        'friends': map(serialize_friend, friends)
    }


class ReportsView(object):

    def __init__(self, account_id, logged_account, elements_per_page=5, page=1):
        self.account = utils.get_account(account_id)
        self.logged_account = logged_account

        self.own_profile = self.account == self.logged_account
        self.elements_per_page = elements_per_page
        self.page = page

    def get_reports_created(self):
        if self.own_profile:
            reports_created = self.account.reports_created.all().order_by('-date_created')
        else:
            reports_created = []

        return self.serialize(reports_created, report_serializer, len(self.account.reports_created.all()))

    def get_reports_received(self):
        if self.own_profile:
            reports_received = self.account.reports_received.all().order_by('-date_created')
        else:
            reports_received = self.account.reports_received.filter(creator=self.logged_account).order_by('-date_created')

        show_report_creator = functools.partial(report_serializer, show_creator_info=not self.own_profile)

        return self.serialize(reports_received, show_report_creator, len(self.account.reports_received.all()))

    def serialize(self, query, serializer_function, total):
        from django.core.paginator import Paginator
        paginator = Paginator(query, self.elements_per_page)
        page = paginator.page(self.page)

        return {
            'reports': map(serializer_function, page),
            'current_page': page.number,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'total': total
        }
