from dota2api import api
from dotaparty import secret
from dota2api.src.exceptions import APITimeoutError

__d2api = api.Initialise(secret.D2_API_KEY)


def get_until_success(get_function):
    while True:
        try:
            import time

            time.sleep(1)
            return get_function()
        except Exception as e:
            import logging

            logging.exception(e)


def get_player_summaries(*args):
    return get_until_success(lambda: __d2api.get_player_summaries(*args))


def get_match_history(account_id, **kwargs):
    return get_until_success(lambda: __d2api.get_match_history(account_id, **kwargs))


def get_match_details(match_id):
    return get_until_success(lambda: __d2api.get_match_details(match_id))


def convert_to_64_bit(number):
    return api.convert_to_64_bit(number)

def get_matches_seq(last_match_id):
    return get_until_success(lambda: __d2api.get_match_history_by_seq_num(last_match_id))
