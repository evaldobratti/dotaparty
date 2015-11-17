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
        if value:
            from core.parameters import INTERESTED_ACCOUNTS_IDS
            INTERESTED_ACCOUNTS_IDS.add_value(self.account_id)

        self._matches_download_required = value

    def as_dict(self):
        return {
            'account_id': self.account_id,
            'steam_id': self.steam_id,
            'profile_url': self.profile_url,
            'current_update': self.current_update.as_dict()
        }


class AccountUpdate(models.Model):
    account = models.ForeignKey(Account, null=False, related_name='updates')
    sequential = models.IntegerField(null=True)
    persona_name = models.CharField(max_length=500, null=True)
    url_avatar = models.CharField(max_length=500, null=True)
    url_avatar_medium = models.CharField(max_length=500, null=True)
    url_avatar_full = models.CharField(max_length=500, null=True)
    primary_clan_id = models.BigIntegerField(null=True)
    persona_state_flags = models.BigIntegerField(null=True)

    def as_dict(self):
        return {
            'persona_name': self.persona_name,
            'url_avatar': self.url_avatar,
            'url_avatar_medium': self.url_avatar_medium,
            'url_avatar_full': self.url_avatar_full
        }


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

    def as_dict(self):
        return {
            'url_image': self.url_image
        }


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

    def as_dict(self):
        return {
            'is_radiant_win': self.is_radiant_win,
            'match_id': self.match_id,
            'start_time': self.start_time,
            'duration': self.duration,
            'first_blood_time': self.first_blood_time,
            'lobby_type': self.lobby_type.name,
            'game_mode': self.game_mode.name,
            'cluster': self.cluster.name,
            'skill': self.skill,
            'radiant_team': map(DetailMatchPlayer.as_dict, self.radiant_team()),
            'dire_team': map(DetailMatchPlayer.as_dict, self.dire_team())
        }


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
        """

        :return: Hero
        """
        return get_hero(self.hero_id)

    def as_dict(self):
        return {
            'level': self.level,
            'kills': self.kills,
            'deaths': self.deaths,
            'assists': self.assists,
            'last_hits': self.last_hits,
            'denies': self.denies,
            'gold_per_min': self.gold_per_min,
            'xp_per_min': self.xp_per_min,
            'gold_spent': self.gold_spent,
            'gold': self.gold,
            'tower_damage': self.tower_damage,
            'hero_damage': self.hero_damage,
            'hero_healing': self.hero_healing,
            'items': map(Item.as_dict, [owner.item() for owner in self.items.all()]),
            'player_account': self.player_account and {
                'account_id': self.player_account.account_id,
                'persona_name': self.player_account.current_update.persona_name,
                'url_avatar': self.player_account.current_update.url_avatar
            },
            'hero': {
                'url_large_portrait': self.hero.url_large_portrait,
                'url_small_portrait': self.hero.url_small_portrait,
                'url_full_portrait': self.hero.url_full_portrait,
                'localized_name': self.hero.localized_name
            }
        }


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
