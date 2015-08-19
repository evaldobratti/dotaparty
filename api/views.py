from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import api_view
from core import utils
from core import tasks
from core.models import Account, DetailMatch
from serializers import DetailMatchSerializer, ProfileSerializer, AccountSerializer
from django.db import transaction
# Create your views here.

@api_view(['GET'])
@transaction.atomic()
def get_details_match(request, match_id):
    return Response(DetailMatchSerializer(utils.get_details_match(match_id)).data)


@api_view(['GET'])
@transaction.atomic()
def get_profile(request, account_id):
    others = request.GET.get('others') and request.GET.get('others').split(',') or []
    account = utils.get_account(account_id)
    return Response(ProfileSerializer(account, others).data)


@api_view(['GET'])
@transaction.atomic()
def get_account(request, account_id):
    return Response(AccountSerializer(utils.get_account(account_id)).data)


@api_view(['GET'])
@transaction.atomic()
def get_accounts_matches(request, accounts_ids):
    page = request.GET.get('page')
    accounts = map(int, accounts_ids.split(','))
    matches_page = utils.get_friends_matches_details(accounts, page)

    return Response({
        'links': {
            'next': matches_page.has_next() and matches_page.next_page_number() or None,
            'previous': matches_page.has_previous() and matches_page.previous_page_number() or None
        },
        'current': matches_page.number,
        'total': matches_page.paginator.num_pages,
        'results': DetailMatchSerializer(matches_page, many=True, accounts=accounts).data
    })


@api_view(['POST'])
def download_games(request, account_id):
    tasks.download_games(account_id)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def find(request, search):
    accounts = Account.objects.filter(current_update__persona_name__icontains=search)
    matches = []
    if search.isdigit():
        accounts = accounts | Account.objects.filter(account_id=int(search))
        matches = DetailMatch.objects.filter(match_id=int(search))

    return Response({
        'accounts': AccountSerializer(accounts, many=True).data,
        'matches': DetailMatchSerializer(matches, many=True).data
    })
