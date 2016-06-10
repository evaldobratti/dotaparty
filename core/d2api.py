import time
import dota2api
import logging
from dotaparty import secret
from dota2api import exceptions

__d2api = dota2api.Initialise(secret.D2_API_KEY)
logger = logging.getLogger('dotaparty.valve')

MAX_RETRIES = 100


def check_tries(tries, exception):
    if tries >= MAX_RETRIES:
        raise exception


def get_until_success(name, get_function):
    tries = 0
    while True:
        try:
            time.sleep(2)
            tries += 1
            logger.info(name)
            return get_function()
        except ValueError as e:
            logger.info(name + ' Time out on api, sleeping some extra seconds')
            time.sleep(30)
            check_tries(tries, e)
        except exceptions.APIError as e:
            logger.error(name + ' ' + e.msg)
            if e.msg == '429':
                time.sleep(2)
            if 'Cannot get match history' in e.msg:
                raise e
            if 'Practice matches' in e.msg:
                raise e
        except Exception as e:
            logger.error(name + ' ' + e.message)
            logger.exception(e)
            check_tries(tries, e)


def get_player_summaries(*args):
    name = 'get_player_summaries ' + str(args)
    return get_until_success(name, lambda: __d2api.get_player_summaries(*args))


def get_match_history(account_id, **kwargs):
    name = 'get_match_history ' + str(account_id) + ' ' + str(kwargs)
    return get_until_success(name, lambda: __d2api.get_match_history(account_id, **kwargs))


def get_match_details(match_id):
    name = 'get_match_details ' + str(match_id)
    return get_until_success(name, lambda: __d2api.get_match_details(match_id))


def to_64b(number):
    return dota2api.convert_to_64_bit(number)


def get_matches_seq(last_match_id):
    name = 'get_match_history_by_seq_num ' + str(last_match_id)
    return get_until_success(name, lambda: __d2api.get_match_history_by_seq_num(last_match_id))


def get_items():
    return get_until_success('get_game_items', lambda: __d2api.get_game_items())


def get_heroes():
    return get_until_success('get_heroes', lambda: __d2api.get_heroes())
