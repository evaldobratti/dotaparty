from django.db import models

items = {}
heroes = {}
abilities = {}


def get_item(item_id):
    if item_id in items:
        return items[item_id]
    else:
        items[item_id] = Item.objects.get(item_id=item_id)
        return items[item_id]


def get_hero(hero_id):
    if hero_id in heroes:
        return heroes[hero_id]
    else:
        heroes[hero_id] = Hero.objects.get(hero_id=hero_id)
        return heroes[hero_id]


def get_ability(ability_id):
    if ability_id in abilities:
        return abilities[ability_id]
    else:
        abilities[ability_id] = Ability.objects.get(ability_id=ability_id)
        return abilities[ability_id]


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
    _matches_download_required = models.BooleanField(null=False, default=False, db_column='matches_download_required')

    @property
    def matches_download_required(self):
        return self._matches_download_required

    @matches_download_required.setter
    def matches_download_required(self, value):
        print '1'
        if value:
            from core.parameters import INTERESTED_ACCOUNTS_IDS
            INTERESTED_ACCOUNTS_IDS.add_value(self.account_id)

        self._matches_download_required = value


class AccountUpdate(models.Model):
    account = models.ForeignKey(Account, null=False, related_name='updates')
    sequential = models.IntegerField(null=True)
    persona_name = models.CharField(max_length=500, null=True)
    url_avatar = models.CharField(max_length=500, null=True)
    url_avatar_medium = models.CharField(max_length=500, null=True)
    url_avatar_full = models.CharField(max_length=500, null=True)
    primary_clan_id = models.BigIntegerField(null=True)
    persona_state_flags = models.BigIntegerField(null=True)


class Hero(models.Model):
    hero_id = models.SmallIntegerField()
    localized_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    url_small_portrait = models.CharField(max_length=300)
    url_large_portrait = models.CharField(max_length=300)
    url_full_portrait = models.CharField(max_length=300)
    url_vertical_portrait = models.CharField(max_length=300)


class Item(models.Model):
    item_id = models.SmallIntegerField(unique=True)
    localized_name = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    is_recipe = models.BooleanField()
    in_secret_shop = models.BooleanField()
    cost = models.SmallIntegerField()
    in_side_shop = models.BooleanField()
    url_image = models.CharField(max_length=400)


class Ability(models.Model):
    ability_id = models.SmallIntegerField()
    name = models.CharField(max_length=100)


class Cluster(models.Model):
    cluster_id = models.IntegerField()
    name = models.CharField(max_length=30)


class LobbyType(models.Model):
    lobby_type_id = models.IntegerField()
    name = models.CharField(max_length=30)


class GameMode(models.Model):
    game_mode_id = models.IntegerField()
    name = models.CharField(max_length=30)


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
    skill = models.PositiveIntegerField(null=True)

    def radiant_team(self):
        return self.players.filter(player_slot__lt=10).order_by('player_slot')

    def dire_team(self):
        return self.players.filter(player_slot__gt=10).order_by('player_slot')


class ItemOwner(models.Model):
    pass


class LeaverStatus(models.Model):
    leaver_id = models.IntegerField(null=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)


class DetailMatchPlayer(ItemOwner):
    player_account = models.ForeignKey(Account, null=True, related_name='match_players')
    match = models.ForeignKey(DetailMatch, null=False, related_name='players')
    account_id = models.BigIntegerField()
    player_slot = models.SmallIntegerField()

    hero_id = models.PositiveIntegerField(null=False)

    kills = models.SmallIntegerField()
    deaths = models.SmallIntegerField()
    assists = models.SmallIntegerField()
    leaver_status = models.ForeignKey(LeaverStatus, null=True)

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

    @property
    def hero(self):
        return get_hero(self.hero_id)


class AdditionalUnit(ItemOwner):
    unit_name = models.CharField(max_length=50)
    player = models.ForeignKey(DetailMatchPlayer, related_name="additional_units")


class DetailMatchOwnerItem(models.Model):
    slot = models.SmallIntegerField()
    owner = models.ForeignKey(ItemOwner, related_name="items")
    item_id = models.PositiveIntegerField(null=False)

    def item(self):
        return get_item(self.item_id)


class DetailMatchAbilityUpgrade(models.Model):
    player = models.ForeignKey(DetailMatchPlayer, related_name='abilities')
    ability_id = models.PositiveIntegerField(null=False)
    time = models.IntegerField()
    upgraded_lvl = models.SmallIntegerField()

    def ability(self):
        return get_ability(self.ability_id)


class Parameter(models.Model):
    name = models.CharField(max_length=40)
    value = models.CharField(max_length=500, null=True)

    def reset(self):
        self.value = None
