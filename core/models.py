from django.db import models
from caching.base import CachingMixin, CachingManager


class Account(models.Model):
    account_id = models.BigIntegerField(unique=True)
    steam_id = models.BigIntegerField(null=True)
    last_logoff = models.BigIntegerField(null=True)
    profile_url = models.CharField(max_length=500, null=True)
    community_visibility_state = models.IntegerField(null=True)
    time_created = models.BigIntegerField(null=True)
    persona_state = models.IntegerField(null=True)
    profile_state = models.IntegerField(null=True)
    current_update = models.ForeignKey('AccountUpdate', related_name='current_update', null=True)


class AccountUpdate(models.Model):
    account = models.ForeignKey(Account, null=False, related_name='updates')
    sequential = models.IntegerField(null=True)
    persona_name = models.CharField(max_length=500, null=True)
    url_avatar = models.CharField(max_length=500, null=True)
    url_avatar_medium = models.CharField(max_length=500, null=True)
    url_avatar_full = models.CharField(max_length=500, null=True)
    primary_clan_id = models.BigIntegerField(null=True)
    persona_state_flags = models.BigIntegerField(null=True)

class Hero(CachingMixin, models.Model):
    hero_id = models.SmallIntegerField()
    localized_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    url_small_portrait = models.CharField(max_length=300)
    url_large_portrait = models.CharField(max_length=300)
    url_full_portrait = models.CharField(max_length=300)
    url_vertical_portrait = models.CharField(max_length=300)

    objects = CachingManager()


class Item(CachingMixin, models.Model):
    item_id = models.SmallIntegerField(unique=True)
    localized_name = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    is_recipe = models.BooleanField()
    in_secret_shop = models.BooleanField()
    cost = models.SmallIntegerField()
    in_side_shop = models.BooleanField()
    url_image = models.CharField(max_length=400)

    objects = CachingManager()


class Ability(CachingMixin, models.Model):
    ability_id = models.SmallIntegerField()
    name = models.CharField(max_length=100)

    objects = CachingManager()


class Cluster(CachingMixin, models.Model):
    cluster_id = models.IntegerField()
    name = models.CharField(max_length=30)

    objects = CachingManager()

class LobbyType(CachingMixin, models.Model):
    lobby_type_id = models.IntegerField()
    name = models.CharField(max_length=30)

    objects = CachingManager()

class GameMode(CachingMixin, models.Model):
    game_mode_id = models.IntegerField()
    name = models.CharField(max_length=30)

    objects = CachingManager()

class DetailMatch(models.Model):
    is_radiant_win = models.BooleanField()
    duration = models.BigIntegerField()
    start_time = models.BigIntegerField()
    match_id = models.BigIntegerField(unique=True)
    match_seq_num = models.BigIntegerField()
    tower_status_radiant = models.SmallIntegerField()
    tower_status_dire = models.SmallIntegerField()
    barracks_status_radiant = models.SmallIntegerField()
    barracks_status_dire = models.SmallIntegerField()
    cluster = models.ForeignKey(Cluster)
    first_blood_time = models.IntegerField()
    lobby_type = models.ForeignKey(LobbyType)
    human_players = models.SmallIntegerField()
    league_id = models.BigIntegerField()
    positive_votes = models.IntegerField()
    negative_votes = models.IntegerField()
    game_mode = models.ForeignKey(GameMode)

    def radiant_team(self):
        return self.players.all().filter(player_slot__lt=10).order_by('player_slot')

    def dire_team(self):
        return self.players.all().filter(player_slot__gt=10).order_by('player_slot')


class ItemOwner(models.Model):
    pass


class LeaverStatus(CachingMixin, models.Model):
    leaver_id = models.IntegerField(null=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    objects = CachingManager()

class DetailMatchPlayer(ItemOwner):
    player_account = models.ForeignKey(Account, null=True, related_name='match_players')
    match = models.ForeignKey(DetailMatch, null=False, related_name='players')
    account_id = models.BigIntegerField()
    player_slot = models.SmallIntegerField()

    hero = models.ForeignKey(Hero)

    kills = models.SmallIntegerField()
    deaths = models.SmallIntegerField()
    assists = models.SmallIntegerField()
    leaver_status = models.ForeignKey(LeaverStatus, null=False)

    gold = models.IntegerField()
    last_hits = models.SmallIntegerField()
    denies = models.SmallIntegerField()
    gold_per_min = models.SmallIntegerField()
    xp_per_min = models.SmallIntegerField()
    gold_spent = models.IntegerField()
    hero_damage = models.IntegerField()
    tower_damage = models.IntegerField()
    hero_healing = models.IntegerField()
    level = models.IntegerField()


class AdditionalUnit(ItemOwner):
    unit_name = models.CharField(max_length=50)
    player = models.ForeignKey(DetailMatchPlayer, related_name="additional_units")


class DetailMatchOwnerItem(models.Model):
    slot = models.SmallIntegerField()
    owner = models.ForeignKey(ItemOwner, related_name="items")
    item = models.ForeignKey(Item)


class DetailMatchAbilityUpgrade(models.Model):
    player = models.ForeignKey(DetailMatchPlayer, related_name='abilities')
    ability = models.ForeignKey(Ability)
    time = models.IntegerField()
    upgraded_lvl = models.SmallIntegerField()
