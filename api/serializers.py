import functools


def account_serializer(account):
    current_update = account.current_update
    return {
        'account_id': account.account_id,
        'steam_id': account.steam_id,
        'profile_url': account.profile_url,
        'current_update': {
            'persona_name': current_update.persona_name,
            'url_avatar': current_update.url_avatar,
            'url_avatar_medium': current_update.url_avatar_medium,
            'url_avatar_full': current_update.url_avatar_full
        }
    }


def item_serializer(item):
    return {
        'url_image': item.url_image
    }


def player_serializer(player):
    return {
        'level': player.level,
        'kills': player.kills,
        'deaths': player.deaths,
        'assists': player.assists,
        'last_hits': player.last_hits,
        'denies': player.denies,
        'gold_per_min': player.gold_per_min,
        'xp_per_min': player.xp_per_min,
        'gold_spent': player.gold_spent,
        'gold': player.gold,
        'tower_damage': player.tower_damage,
        'hero_damage': player.hero_damage,
        'hero_healing': player.hero_healing,
        'items': map(item_serializer, [owner.item() for owner in player.items.all()]),
        'player_account': player.player_account and {
            'account_id': player.player_account.account_id,
            'persona_name': player.player_account.current_update.persona_name,
            'url_avatar': player.player_account.current_update.url_avatar
        },
        'hero': {
            'url_large_portrait': player.hero.url_large_portrait,
            'url_small_portrait': player.hero.url_small_portrait,
            'url_full_portrait': player.hero.url_full_portrait,
            'localized_name': player.hero.localized_name
        }
    }


def detail_match_serializer(match, accounts_ids=[]):
    radiant_team = match.radiant_team()
    dire_team = match.dire_team()

    if accounts_ids:
        radiant_team = match.radiant_team().filter(player_account__account_id__in=accounts_ids)
        dire_team = match.dire_team().filter(player_account__account_id__in=accounts_ids)

    return {
        'is_radiant_win': match.is_radiant_win,
        'match_id': match.match_id,
        'start_time': match.start_time,
        'duration': match.duration,
        'first_blood_time': match.first_blood_time,
        'lobby_type': match.lobby_type.name,
        'game_mode': match.game_mode.name,
        'cluster': match.cluster.name,
        'skill': match.skill,
        'radiant_team': map(player_serializer, radiant_team),
        'dire_team': map(player_serializer, dire_team)
    }


def details_match_from_players_serializer(accounts_ids):
    return functools.partial(detail_match_serializer, accounts_ids=accounts_ids)
