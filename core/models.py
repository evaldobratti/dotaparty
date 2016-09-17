from django.db import models
from django.utils import timezone

items = {}
heroes = {}


def get_item(item_id):
    if len(items) == 0:
        for item in Item.objects.all():
            items[item.item_id] = item

    return items[item_id]


def get_hero(hero_id):
    if len(heroes) == 0:
        for hero in Hero.objects.all():
            heroes[hero.hero_id] = hero

    return heroes[hero_id]


class Account(models.Model):
    account_id = models.BigIntegerField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
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

    def __unicode__(self):
        return unicode(self.account_id)


class AccountUpdate(models.Model):
    account = models.ForeignKey(Account, null=False, related_name='updates')
    sequential = models.IntegerField(null=True, blank=True)
    persona_name = models.CharField(max_length=500, null=True)
    url_avatar = models.CharField(max_length=500, null=True)
    url_avatar_medium = models.CharField(max_length=500, null=True)
    url_avatar_full = models.CharField(max_length=500, null=True)
    primary_clan_id = models.BigIntegerField(null=True, blank=True)
    persona_state_flags = models.BigIntegerField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super(AccountUpdate, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        unique_together = ('account',
                           'persona_name',
                           'url_avatar',
                           'url_avatar_medium',
                           'url_avatar_full',
                           'primary_clan_id',
                           'persona_state_flags')


class Hero(models.Model):
    hero_id = models.SmallIntegerField(unique=True, db_index=True)
    localized_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    url_small_portrait = models.CharField(max_length=300)
    url_large_portrait = models.CharField(max_length=300)
    url_full_portrait = models.CharField(max_length=300)
    url_vertical_portrait = models.CharField(max_length=300)


class Item(models.Model):
    item_id = models.SmallIntegerField(unique=True)
    localized_name = models.CharField(max_length=400)
    name = models.CharField(max_length=40)
    is_recipe = models.BooleanField()
    in_secret_shop = models.BooleanField()
    cost = models.SmallIntegerField()
    in_side_shop = models.BooleanField()
    url_image = models.CharField(max_length=400)


class Cluster(models.Model):
    cluster_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)


class LobbyType(models.Model):
    lobby_type_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)


class GameMode(models.Model):
    game_mode_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)


class DetailMatch(models.Model):
    SKILL_LEVEL_CHOICE = ((None, "To be determined"),
                          (1, "Normal"),
                          (2, "High"),
                          (3, "Very High"),
                          (4, "Not determined"))

    is_radiant_win = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    duration = models.BigIntegerField()
    start_time = models.BigIntegerField()
    match_id = models.BigIntegerField(unique=True, db_index=True)
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
    skill = models.PositiveIntegerField(null=True, choices=SKILL_LEVEL_CHOICE)

    @classmethod
    def with_related(cls):
        query = cls.objects.all()
        query = query.select_related("cluster")
        query = query.select_related("lobby_type")
        query = query.select_related("game_mode")
        query = query.prefetch_related("players__player_account__current_update")
        query = query.prefetch_related("players__abilities")
        query = query.prefetch_related("players__items")
        return query

    def radiant_team(self):
        return self.players.filter(player_slot__lt=10).order_by('player_slot')

    def dire_team(self):
        return self.players.filter(player_slot__gt=10).order_by('player_slot')

    def __unicode__(self):
        return str(self.match_id)


class ItemOwner(models.Model):
    pass


class LeaverStatus(models.Model):
    leaver_id = models.IntegerField(null=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)


class DetailMatchPlayer(ItemOwner):
    player_account = models.ForeignKey(Account, null=True, related_name='match_players')
    match = models.ForeignKey(DetailMatch, null=False, related_name='players')
    account_id = models.BigIntegerField(db_index=True)
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


class Parameter(models.Model):
    name = models.CharField(max_length=40)
    value = models.CharField(max_length=500, null=True)

    def reset(self):
        self.value = None


class Visit(models.Model):
    host = models.CharField(max_length=400)
    requested = models.CharField(max_length=400)
    last_visit = models.DateTimeField(auto_now=True)
    count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return '{:<15} {:<15} {:<3} {:<30}'.format(self.host, self.requested, self.count, self.last_visit)


class Proxy(models.Model):
    address = models.CharField(max_length=100)
    successes = models.PositiveIntegerField(default=0)
    failures = models.PositiveIntegerField(default=0)
    timeouts = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    last_success = models.DateTimeField(auto_now_add=True)

    def increase_failures(self):
        delta = timezone.now() - self.last_success
        if delta.days >= 2:
            self.active = False

        self.failures = models.F('failures') + 1

    def increase_successes(self):
        self.last_success = timezone.now()
        self.successes = models.F('successes') + 1

    def increase_timeouts(self):
        if self.timeouts >= 10:
            self.active = False
        self.timeouts = models.F('timeouts') + 1
