from models import *
from dota2api import api
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dotaparty import secret

d2api = api.Initialise(secret.D2_API_KEY)


def get_until_success(get_function):
    while True:
        try:
            import time

            time.sleep(1)
            return get_function()
        except Exception as e:
            import logging

            logging.exception(e)


def get_account(account_id):
    account = Account.objects.filter(account_id=account_id)
    if account:
        return account[0]
    else:
        acc = get_until_success(lambda: d2api.get_player_summaries(*[int(account_id)]))

        if acc:
            return load_account(account_id, acc[0])
        return None


def load_account(account_id, updated_acc):
    account, _ = Account.objects.get_or_create(account_id=account_id)
    account.steam_id = updated_acc.steam_id
    account.last_logoff = updated_acc.last_logoff
    account.profile_url = updated_acc.profile_url
    account.community_visibility_state = updated_acc.community_visibility_state
    account.time_created = updated_acc.time_created
    account.persona_state = updated_acc.persona_state
    account.profile_state = updated_acc.profile_state
    update, created = account.updates.get_or_create(account=account,
                                                    persona_name=updated_acc.persona_name,
                                                    url_avatar=updated_acc.url_avatar,
                                                    url_avatar_medium=updated_acc.url_avatar_medium,
                                                    url_avatar_full=updated_acc.url_avatar_full,
                                                    primary_clan_id=updated_acc.primary_clan_id,
                                                    persona_state_flags=updated_acc.persona_state_flags)
    account.current_update = update
    account.save()
    if created:
        update.sequential = len(account.updates.all())
        update.save()

    return account


def load_team(match, players):
    updated_accounts = get_until_success(lambda: d2api.get_player_summaries(*[p.account_id for p in players]))
    for player_response in players:
        hero, _ = Hero.objects.get_or_create(hero_id=player_response.hero.id,
                                             localized_name=player_response.hero.localized_name,
                                             name=player_response.hero.name,
                                             url_small_portrait=player_response.hero.url_small_portrait,
                                             url_large_portrait=player_response.hero.url_large_portrait,
                                             url_full_portrait=player_response.hero.url_full_portrait,
                                             url_vertical_portrait=player_response.hero.url_vertical_portrait)

        if player_response.account_id != 4294967295 and player_response.account_id != -1:
            updated_acc = [ua for ua in updated_accounts
                           if str(ua.steam_id) == str(api.convert_to_64_bit(player_response.account_id))][0]
            account = load_account(player_response.account_id, updated_acc)
        else:
            account = None

        leaver_status, _ = LeaverStatus.objects.get_or_create(leaver_id=player_response.leaver_status.id,
                                                              name=player_response.leaver_status.name,
                                                              description=player_response.leaver_status.description)

        player = DetailMatchPlayer.objects.create(match=match, player_account=account,
                                                  account_id=player_response.account_id,
                                                  player_slot=player_response.player_slot,
                                                  hero_id=hero.hero_id, kills=player_response.kills,
                                                  deaths=player_response.deaths, assists=player_response.assists,
                                                  leaver_status=leaver_status,
                                                  gold=player_response.gold,
                                                  last_hits=player_response.last_hits, denies=player_response.denies,
                                                  gold_per_min=player_response.gold_per_min,
                                                  xp_per_min=player_response.xp_per_min,
                                                  gold_spent=player_response.gold_spent,
                                                  hero_damage=player_response.hero_damage,
                                                  tower_damage=player_response.tower_damage,
                                                  hero_healing=player_response.hero_healing,
                                                  level=player_response.level)

        for additional_unit in player_response.additional_units:
            unit, unit_created = AdditionalUnit.objects.get_or_create(unit_name=additional_unit.unit_name,
                                                                      player=player)
            for index, item_response in enumerate(additional_unit.items):
                item, _ = Item.objects.get_or_create(item_id=item_response.id,
                                                     localized_name=item_response.localized_name,
                                                     name=item_response.name,
                                                     is_recipe=bool(item_response.is_recipe),
                                                     in_secret_shop=item_response.in_secret_shop,
                                                     cost=item_response.cost,
                                                     in_side_shop=item_response.in_side_shop,
                                                     url_image=item_response.url_image)

                DetailMatchOwnerItem.objects.create(owner=unit, slot=index, item_id=item.item_id)

        for index, item_response in enumerate(player_response.items):
            item, _ = Item.objects.get_or_create(item_id=item_response.id,
                                                 localized_name=item_response.localized_name,
                                                 name=item_response.name,
                                                 is_recipe=bool(item_response.is_recipe),
                                                 in_secret_shop=item_response.in_secret_shop,
                                                 cost=item_response.cost,
                                                 in_side_shop=item_response.in_side_shop,
                                                 url_image=item_response.url_image)

            DetailMatchOwnerItem.objects.create(owner=player, slot=index, item_id=item.item_id)

        for upgrade in player_response.ability_upgrades:
            ability, _ = Ability.objects.get_or_create(ability_id=upgrade.ability,
                                                       name=upgrade.ability_name)
            DetailMatchAbilityUpgrade.objects.create(player=player,
                                                     ability_id=ability.ability_id,
                                                     time=upgrade.time,
                                                     upgraded_lvl=upgrade.level)


def parse_from_details_match(match_details):
    cluster, _ = Cluster.objects.get_or_create(cluster_id=match_details.cluster,
                                               name=match_details.cluster_name)

    game_mode, _ = GameMode.objects.get_or_create(game_mode_id=match_details.game_mode,
                                                  name=match_details.game_mode_name)

    lobby_type, _ = LobbyType.objects.get_or_create(lobby_type_id=match_details.lobby_type,
                                                    name=match_details.lobby_name)

    match = DetailMatch.objects.create(is_radiant_win=match_details.is_radiant_win, duration=match_details.duration,
                                       start_time=match_details.start_time, match_id=match_details.match_id,
                                       match_seq_num=match_details.match_seq_num,
                                       tower_status_radiant=match_details.tower_status_radiant,
                                       tower_status_dire=match_details.tower_status_dire,
                                       barracks_status_radiant=match_details.barracks_status_radiant,
                                       barracks_status_dire=match_details.barracks_status_dire,
                                       cluster=cluster,
                                       first_blood_time=match_details.first_blood_time,
                                       lobby_type=lobby_type,
                                       human_players=match_details.human_players, league_id=match_details.league_id,
                                       positive_votes=match_details.positive_votes,
                                       negative_votes=match_details.negative_votes,
                                       game_mode=game_mode)

    load_team(match, match_details.players)

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
        details = get_until_success(lambda: d2api.get_match_details(match_id))
        return parse_from_details_match(details)


def get_friends_number_matches(account, compared_to=[]):
    friends_query = len(compared_to) > 0 \
                    and ' AND dmp2.account_id IN (' + ','.join(compared_to) + ')' \
                    or ''

    query = 'SELECT dmp2.player_account_id AS id, ' + \
            '       acc2.account_id as account_id, ' + \
            '       accup2.persona_name, ' + \
            '       count(*) AS qtd ' + \
            'FROM core_account acc ' + \
            'JOIN core_detailmatchplayer dmp1 ON acc.id = dmp1.player_account_id ' + \
            'JOIN core_detailmatchplayer dmp2 ON dmp1.match_id = dmp2.match_id ' + \
            'JOIN core_account acc2 ON dmp2.player_account_id = acc2.id ' + \
            'JOIN core_accountupdate accup2 ON acc2.current_update_id = accup2.id ' + \
            'WHERE dmp1.player_account_id = ' + str(account.id) + ' ' + \
            '  AND (dmp2.player_account_id <> ' + str(account.id) + friends_query + ')' + \
            'GROUP BY dmp1.player_account_id, ' + '         acc2.account_id, ' + '         accup2.persona_name, ' + \
            '         dmp2.player_account_id '

    if not len(compared_to):
        query += 'HAVING count(*) > 1 '

    query += 'ORDER BY count(*) DESC '
    raw = Account.objects.raw(
        query
    )

    return raw


def get_friends_matches_details(accounts_ids, page):
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

    paginator = Paginator(query, 10)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
