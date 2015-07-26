from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import api_view
from core import utils
from core import tasks
from core.models import Account
from serializers import DetailMatchSerializer, ProfileSerializer, AccountSerializer
# Create your views here.

@api_view(['GET'])
def get_details_match(request, match_id):
    return Response(DetailMatchSerializer(utils.get_details_match(match_id)).data)

@api_view(['GET'])
def get_profile(request, account_id):
    return Response(ProfileSerializer(Account.objects.get(account_id=account_id)).data)

@api_view(['GET'])
def get_account(request, account_id):
    return Response(AccountSerializer(Account.objects.get(account_id=account_id)).data)

@api_view(['GET'])
def get_friends_matches_details(request, accounts_ids):
    return Response(DetailMatchSerializer(utils.get_friends_matches_details(accounts_ids.split(',')), many=True).data)

@api_view(['POST'])
def download_games(request, account_id):
    tasks.download_games(account_id)
    return Response(status=status.HTTP_200_OK)
