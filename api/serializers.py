from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from core.models import DetailMatch, DetailMatchPlayer, Hero, Account, Item, DetailMatchAbilityUpgrade, DetailMatchOwnerItem, Cluster, LobbyType, GameMode, AccountUpdate
from core.utils import get_friends_number_matches

class ClusterSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Cluster


class LobbyTypeSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = LobbyType


class GameModeSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = GameMode


class DetailMatchAbilityUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailMatchAbilityUpgrade


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item


class DetailMatchOwnerItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = DetailMatchOwnerItem

class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUpdate


class AccountSerializer(serializers.ModelSerializer):
    current_update = AccountUpdateSerializer()

    class Meta:
        model = Account


class PlayerSerializer(serializers.ModelSerializer):
    hero = HeroSerializer()
    player_account = AccountSerializer()
    items = DetailMatchOwnerItemSerializer(many=True)
    abilities = DetailMatchAbilityUpgradeSerializer(many=True)

    class Meta:
        model = DetailMatchPlayer


class DefaultPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DetailMatchSerializer(serializers.ModelSerializer):
    radiant_team = PlayerSerializer(many=True)
    dire_team = PlayerSerializer(many=True)
    lobby_type = LobbyTypeSerialiazer()
    game_mode = GameModeSerialiazer()
    cluster = ClusterSerialiazer()

    class Meta:
        model = DetailMatch


class FriendSerializer(serializers.BaseSerializer):
    def to_representation(self, account):
        return {'account_id': account.account_id,
                'persona_name': account.persona_name,
                'qtd': account.qtd
                }


class ProfileSerializer(serializers.BaseSerializer):
    def to_representation(self, account):
        friends = get_friends_number_matches(account)
        return {
            'account_id': account.account_id,
            'persona_name': account.current_update.persona_name,
            'url_avatar': account.current_update.url_avatar,
            'friends': FriendSerializer(friends, many=True).data
        }