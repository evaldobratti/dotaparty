from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core import utils
from core.models import Account
from serializers import DetailMatchSerializer, ProfileSerializer
# Create your views here.

@api_view(['GET'])
def get_details_match(request, match_id):
    return Response(DetailMatchSerializer(utils.get_details_match(match_id)).data)

@api_view(['GET'])
def get_profile(request, account_id):
    return Response(ProfileSerializer(Account.objects.get(account_id=account_id)).data)