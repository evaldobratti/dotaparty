import json

from core import utils
from core import tasks
from core.models import Account, DetailMatch
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.db import transaction
from django.contrib import auth
from django.shortcuts import redirect
from django.http import JsonResponse
from community import models as cm
import serializers
import datetime
from core import parameters
from core import utils


@transaction.atomic()
def get_details_match(request, match_id):
    match = utils.get_details_match(match_id)
    return JsonResponse(serializers.detail_match_serializer(match))


def get_profile(request, account_id):
    others = request.GET.get('others') and request.GET.get('others').split(',') or []
    account = utils.get_account(account_id)

    if str(request.GET.get('includeFriends')).lower() == 'true' or others:
        friends = utils.get_friends_number_matches(account, others)
    else:
        friends = []

    serialized = serializers.account_serializer(account)

    if friends:
        serialized['friends'] = []
        for f in friends:
            friend = serializers.account_serializer(f)
            friend['qtd'] = f.qtd

            serialized['friends'].append(friend)

    return JsonResponse(serialized)


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


def find(request):
    search = request.GET['query']

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

    report = cm.Report()
    report.creator = creator
    report.reported = reported
    report.due_to_match = match
    report.reason = reason

    try:
        report.save()
    except ValidationError, exc:
        return JsonResponse({
            'error': exc.messages
        }, status=400)

    return HttpResponse()


def get_authenticated_user(request):
    if request.user.is_authenticated():
        serialized = serializers.account_serializer(request.user.account)
        serialized['is_authenticated'] = True
        return JsonResponse(serialized)

    return JsonResponse({
        'is_authenticated': False
    })


def get_statistics(request):
    matches = DetailMatch.objects.order_by('-created_at')[:10]
    last_matches = []

    for match in matches:
        players = []
        for player in match.players.filter(account_id__in=parameters.INTERESTED_ACCOUNTS_IDS.value()):
            players.append({
                'account_id': player.account_id,
                'persona_name': player.player_account.current_update.persona_name
            })
        last_matches.append({
            'match_id': match.match_id,
            'players': players
        })

    return JsonResponse({
        'total': {
            'matches': len(DetailMatch.objects.all()),
            'players': len(Account.objects.all()),
            'tracked': len(parameters.INTERESTED_ACCOUNTS_IDS.value())
        },
        'last_hour': {
            'matches': len(DetailMatch.objects.filter(created_at__gt=datetime.datetime.now() - datetime.timedelta(hours=1))),
            'players': len(Account.objects.filter(created_at__gt=datetime.datetime.now() - datetime.timedelta(hours=1)))
        },
        'lasts_matches': last_matches

    })