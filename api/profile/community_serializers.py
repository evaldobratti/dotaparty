import datetime
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


def report_serializer(report):
    return {
        'created': seconds_since_epoch(report.date_created),
        'creator': account_serializer(report.creator),
        'reported': account_serializer(report.reported),
        'reason': report.reason,
        'due_to_match_id': report.due_to_match.match_id
    }


def profile_serializer(account_id, others_accounts_ids, logged_account):
    account = utils.get_account(account_id)
    friends = utils.get_friends_number_matches(account, others_accounts_ids)

    if account != logged_account:
        reports_received = account.reports_received.filter(creator=logged_account).order_by('-date_created')
        reports_created = account.reports_created.filter(reported=logged_account).order_by('-date_created')
    else:
        reports_created = account.reports_created.all().order_by('-date_created')
        reports_received = account.reports_received.all().order_by('-date_created')

    return {
        'account_id': account.account_id,
        'persona_name': account.current_update.persona_name,
        'url_avatar': account.current_update.url_avatar,
        'reports_created': map(report_serializer, reports_created),
        'reports_received': map(report_serializer, reports_received),
        'friends': map(serialize_friend, friends),
        'number_reports_created': len(account.reports_created.all()),
        'number_reports_received': len(account.reports_received.all())
    }
