import dota2api
import logging
from dotaparty import secret

__d2api = dota2api.Initialise(secret.D2_API_KEY)
logger = logging.getLogger('valveapi')

def get_until_success(get_function):
    while True:
        try:
            import time

            time.sleep(1)
            return get_function()
        except ValueError as e:
            logger.info('Time out on api, sleeping 1 extra second')
            time.sleep(1)
        except Exception as e:
            logging.exception(e)


def get_player_summaries(*args):
    return get_until_success(lambda: __d2api.get_player_summaries(*args))


def get_match_history(account_id, **kwargs):
    return get_until_success(lambda: __d2api.get_match_history(account_id, **kwargs))


def get_match_details(match_id):
    return get_until_success(lambda: __d2api.get_match_details(match_id))


def to_64b(number):
    return dota2api.convert_to_64_bit(number)


def get_matches_seq(last_match_id):
    return get_until_success(lambda: __d2api.get_match_history_by_seq_num(last_match_id))


def get_items():
    return get_until_success(lambda: __d2api.get_game_items())


def get_heroes():
    return get_until_success(lambda: __d2api.get_heroes())
