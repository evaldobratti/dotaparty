from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dotaparty import secret
from core import d2api

PRIVATE_PROFILE_ACCOUNT_ID = 4294967295


def get_account(account_id):
    account = Account.objects.filter(account_id=account_id)
    if account:
        return account[0]
    else:
        acc = d2api.get_player_summaries(*[int(account_id)])

        if acc:
            return load_account(account_id, acc['players'][0])
        return None


def load_account(account_id, update):
    acc, _ = Account.objects.get_or_create(account_id=account_id)
    acc.steam_id = update['steamid']
    acc.last_logoff = update['lastlogoff']
    acc.profile_url = update['profileurl']
    acc.community_visibility_state = update['communityvisibilitystate']
    acc.time_created = update.get('timecreated')
    acc.persona_state = update['personastate']
    acc.profile_state = update.get('profilestate')
    current_update, created = acc.updates.get_or_create(account=acc,
                                                        persona_name=update['personaname'],
                                                        url_avatar=update['avatar'],
                                                        url_avatar_medium=update['avatarmedium'],
                                                        url_avatar_full=update['avatarfull'],
                                                        primary_clan_id=update.get('primaryclanid'),
                                                        persona_state_flags=update.get('personastateflags'))
    acc.current_update = current_update
    acc.save()
    if created:
        current_update.sequential = len(acc.updates.all())
        current_update.save()

    return acc


def load_team(match, players):
    updated_accounts = d2api.get_player_summaries(*[p.get('account_id') for p in players])['players']
    for p in players:
        if p.get('account_id', -1) != PRIVATE_PROFILE_ACCOUNT_ID and p.get('account_id', -1) != -1:
            def filtro(ua):
                return str(ua['steamid']) == str(d2api.to_64b(p['account_id']))

            update = filter(filtro, updated_accounts)[0]

            account = load_account(p['account_id'], update)
        else:
            account = None

        if p.get('leaver_status') is None:
            leaver_status = None
        else:
            leaver_status, _ = LeaverStatus.objects.get_or_create(leaver_id=p['leaver_status'],
                                                                  name=p['leaver_status_name'],
                                                                  description=p['leaver_status_description'])

        player = DetailMatchPlayer.objects.create(match=match,
                                                  player_account=account,
                                                  account_id=p['account_id'],
                                                  player_slot=p['player_slot'],
                                                  hero_id=p['hero_id'],
                                                  kills=p['kills'],
                                                  deaths=p.get("deaths", p.get('death')),
                                                  assists=p['assists'],
                                                  leaver_status=leaver_status,
                                                  gold=p.get('gold', 0),
                                                  last_hits=p['last_hits'],
                                                  denies=p['denies'],
                                                  gold_per_min=p['gold_per_min'],
                                                  xp_per_min=p['xp_per_min'],
                                                  gold_spent=p.get('gold_spent', 0),
                                                  hero_damage=p.get('hero_damage', 0),
                                                  tower_damage=p.get('tower_damage', 0),
                                                  hero_healing=p.get('hero_healing',0),
                                                  level=p['level'])

        for additional_unit in p.get('additional_units', []):
            unit, _ = AdditionalUnit.objects.get_or_create(unit_name=additional_unit['unitname'],
                                                           player=player)
            for i in range(0, 5):
                DetailMatchOwnerItem.objects.create(owner=unit, slot=i, item_id=additional_unit['item_' + str(i)])

        for i in range(0, 5):
            DetailMatchOwnerItem.objects.create(owner=player, slot=i, item_id=p['item_' + str(i)])

        for upgrade in p.get('ability_upgrades', []):
            DetailMatchAbilityUpgrade.objects.create(player=player,
                                                     ability_id=upgrade['ability'],
                                                     time=upgrade['time'],
                                                     upgraded_lvl=upgrade['level'])


def get_or_create_item(item_response):
    try:
        return Item.objects.get(item_id=item_response['id'])
    except Item.DoesNotExist:
        return Item.objects.get_or_create(item_id=item_response['id'],
                                          localized_name=item_response['localized_name'],
                                          name=item_response['name'],
                                          is_recipe=bool(item_response['is_recipe']),
                                          in_secret_shop=item_response['in_secret_shop'],
                                          cost=item_response['cost'],
                                          in_side_shop=item_response['in_side_shop'],
                                          url_image=item_response['url_image'])[0]


def parse(match_details):
    cluster, _ = Cluster.objects.get_or_create(cluster_id=match_details['cluster'],
                                               name=match_details['cluster_name'])

    game_mode, _ = GameMode.objects.get_or_create(game_mode_id=match_details['game_mode'],
                                                  name=match_details['game_mode_name'])

    lobby_type, _ = LobbyType.objects.get_or_create(lobby_type_id=match_details['lobby_type'],
                                                    name=match_details['lobby_name'])

    match = DetailMatch.objects.create(is_radiant_win=match_details['radiant_win'], duration=match_details['duration'],
                                       start_time=match_details['start_time'], match_id=match_details['match_id'],
                                       match_seq_num=match_details['match_seq_num'],
                                       tower_status_radiant=match_details['tower_status_radiant'],
                                       tower_status_dire=match_details['tower_status_dire'],
                                       barracks_status_radiant=match_details['barracks_status_radiant'],
                                       barracks_status_dire=match_details['barracks_status_dire'],
                                       cluster=cluster,
                                       first_blood_time=match_details['first_blood_time'],
                                       lobby_type=lobby_type,
                                       human_players=match_details['human_players'], league_id=match_details['leagueid'],
                                       positive_votes=match_details['positive_votes'],
                                       negative_votes=match_details['negative_votes'],
                                       game_mode=game_mode)

    load_team(match, match_details['players'])

    return match


def get_details_match(match_id):
    query = DetailMatch.objects.filter(match_id=match_id)
    query = query.select_related("cluster")
    query = query.select_related("lobby_type")
    query = query.select_related("game_mode")
    query = query.prefetch_related("players__player_account__current_update")
    query = query.prefetch_related("players__abilities")
    query = query.prefetch_related("players__items")
    if query:
        return query[0]
    else:
        details = d2api.get_match_details(match_id)
        return parse(details)


def get_friends_number_matches(account, compared_to=[]):
    friends_query = len(compared_to) > 0 \
                    and ' AND dmp2.account_id IN (' + ','.join(compared_to) + ')' \
                    or ''

    query = 'SELECT dmp2.player_account_id AS id, ' + \
            '       acc2.account_id as account_id, ' + \
            '       accup2.url_avatar as url_avatar, ' + \
            '       accup2.persona_name, ' + \
            '       count(*) AS qtd ' + \
            'FROM core_account acc ' + \
            'JOIN core_detailmatchplayer dmp1 ON acc.id = dmp1.player_account_id ' + \
            'JOIN core_detailmatchplayer dmp2 ON dmp1.match_id = dmp2.match_id ' + \
            'JOIN core_account acc2 ON dmp2.player_account_id = acc2.id ' + \
            'JOIN core_accountupdate accup2 ON acc2.current_update_id = accup2.id ' + \
            'WHERE dmp1.player_account_id = ' + str(account.id) + ' ' + \
            '  AND (dmp2.player_account_id <> ' + str(account.id) + friends_query + ')' + \
            'GROUP BY dmp1.player_account_id, ' + '         acc2.account_id, ' + 'accup2.url_avatar' \
                                                                                 ', accup2.persona_name, ' + \
            '         dmp2.player_account_id '

    if not len(compared_to):
        query += 'HAVING count(*) > 1 '

    query += 'ORDER BY count(*) DESC LIMIT 12 '
    raw = Account.objects.raw(
        query
    )

    return raw


def get_friends_matches_details(accounts_ids, page, elements_per_page=10):
    query = DetailMatch.objects.distinct()
    query = query.select_related("cluster")
    query = query.select_related("lobby_type")
    query = query.select_related("game_mode")
    query = query.prefetch_related("players__player_account__current_update")
    query = query.prefetch_related("players__abilities")
    query = query.prefetch_related("players__items")
    query = query.order_by('-start_time')
    for account_id in accounts_ids:
        query = query.filter(players__player_account__account_id=account_id)

    paginator = Paginator(query, elements_per_page)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def update_items():
    for item_response in d2api.get_items()['items']:
        print item_response['localized_name']
        try:
            my_item = Item.objects.get(item_id=item_response['id'])
            my_item.localized_name = item_response['localized_name']
            my_item.name = item_response['name']
            my_item.is_recipe = bool(item_response['recipe'])
            my_item.in_secret_shop = bool(item_response['secret_shop'])
            my_item.cost = item_response['cost']
            my_item.in_side_shop = bool(item_response['side_shop'])
            my_item.url_image = item_response['url_image']
            my_item.save()
            print my_item.localized_name
        except Item.DoesNotExist:
            pass


def update_heroes():
    for hero_response in d2api.get_heroes()['heroes']:
        print hero_response['localized_name']
        try:
            hero = Hero.objects.get(hero_id=hero_response['id'])
            hero.hero_id = hero_response['id']
            hero.localized_name = hero_response['localized_name']
            hero.name = hero_response['name']
            hero.url_small_portrait = hero_response['url_small_portrait']
            hero.url_large_portrait = hero_response['url_large_portrait']
            hero.url_full_portrait = hero_response['url_full_portrait']
            hero.url_vertical_portrait = hero_response['url_vertical_portrait']
            hero.save()
        except Hero.DoesNotExist:
            Hero.objects.get_or_create(hero_id=hero_response['id'],
                                       localized_name=hero_response['localized_name'],
                                       name=hero_response['name'],
                                       url_small_portrait=hero_response['url_small_portrait'],
                                       url_large_portrait=hero_response['url_large_portrait'],
                                       url_full_portrait=hero_response['url_full_portrait'],
                                       url_vertical_portrait=hero_response['url_vertical_portrait'])
