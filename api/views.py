import json

from core import utils
from core import tasks
from core.models import Account, DetailMatch
from django.http import HttpResponse
from django.db import transaction
from django.contrib import auth
from django.shortcuts import redirect
from django.http import JsonResponse
from community import models as cm
from profile import community_serializers
import serializers


@transaction.atomic()
def get_details_match(request, match_id):
    match = utils.get_details_match(match_id)
    return JsonResponse(serializers.detail_match_serializer(match))


def get_profile(request, account_id):
    others = request.GET.get('others') and request.GET.get('others').split(',') or []
    logged_user = request.user.account if request.user.is_authenticated() else None
    return JsonResponse(community_serializers.profile_serializer(account_id, others, logged_user))


def get_account(request, account_id):
    account = utils.get_account(account_id)
    return JsonResponse({
        'persona_name': account.current_update.persona_name,
        'url_avatar': account.current_update.url_avatar,
        'account_id': account.account_id
    })


def get_accounts_matches(request, comma_accounts_ids):
    page = request.GET.get('page')
    accounts = map(int, comma_accounts_ids.split(','))
    matches_page = utils.get_friends_matches_details(accounts, page)

    return JsonResponse({
        'links': {
            'next': matches_page.has_next() and matches_page.next_page_number() or None,
            'previous': matches_page.has_previous() and matches_page.previous_page_number() or None
        },
        'current': matches_page.number,
        'total': matches_page.paginator.num_pages,
        'results': map(serializers.details_match_from_players_serializer(accounts), matches_page)
    })


def download_games(request, account_id):
    account = Account.objects.get(account_id=int(account_id))
    tasks.download_games(account)
    account.matches_download_required = True
    account.save()

    return HttpResponse()


def find(request, search):
    accounts = Account.objects.filter(current_update__persona_name__icontains=search)
    matches = []
    if search.isdigit():
        accounts = accounts | Account.objects.filter(account_id=int(search))
        matches = DetailMatch.objects.filter(match_id=int(search))

    return JsonResponse({
        'accounts': map(serializers.account_serializer, accounts),
        'matches': map(serializers.detail_match_serializer, matches)
    })


def logout(request):
    auth.logout(request)

    return redirect(request.GET['next'])


def new_report(request):
    data = json.loads(request.body)
    creator = cm.Account.objects.get(account_id=request.user.account_id)
    reported = cm.Account.objects.get(account_id=int(data['reported']))
    match = DetailMatch.objects.get(match_id=int(data['matchId']))
    reason = data['reason']

    cm.Report.objects.create(creator=creator,
                             reported=reported,
                             reason=reason,
                             due_to_match=match)

    return HttpResponse()


def get_authenticated_user(request):
    if request.user.is_authenticated():
        serialized = serializers.account_serializer(request.user.account)
        serialized['is_authenticated'] = True
        return JsonResponse(serialized)

    return JsonResponse({
        'is_authenticated': False
    })
