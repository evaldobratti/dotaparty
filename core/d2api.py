import time
import dota2api
import logging
import itertools
import requests
from dotaparty import secret
from dota2api import exceptions
from threading import Lock
from .models import Proxy
from requests.exceptions import ConnectionError
from requests.exceptions import ConnectTimeout


class D2Api(object):

    MAX_RETRIES = 100

    def __init__(self, logger=logging.getLogger('dotaparty.valve'), use_proxy=False, wait=1):
        self.use_proxy = use_proxy
        self.keys = itertools.cycle(secret.D2_API_KEYS)
        self.logger = logger
        self.lock = Lock()
        self.wait = wait

    def check_tries(self, tries, exception):
        if tries >= D2Api.MAX_RETRIES:
            raise exception

    def api(self):
        def get(url):
            proxy = Proxy.objects.filter(active=True).order_by('?').first()
            address = proxy.address
            proxies = {'http': address}
            try:
                result = requests.get(url, proxies=proxies, timeout=3)
                proxy.increase_successes()
                return result
            except ConnectTimeout as e:
                proxy.increase_timeouts()
                raise e
            except Exception as e:
                proxy.increase_failures()
                raise e
            finally:
                proxy.save()

        if self.use_proxy:
            return dota2api.Initialise(self.keys.next(), executor=get)
        else:
            return dota2api.Initialise(self.keys.next())

    def get_until_success(self, name, get_function):
        tries = 0
        while True:
            try:
                self.lock.acquire()
                time.sleep(self.wait)
                tries += 1
                self.logger.info(name)
                value = get_function()
                self.lock.release()
                return value
            except ValueError as e:
                self.lock.release()
                self.logger.info(name + ' Time out on api, sleeping some extra seconds')
                self.check_tries(tries, e)
                time.sleep(self.wait)
            except exceptions.APIError as e:
                self.lock.release()
                self.logger.error(name + ' ' + str(type(e)) + ' ' + e.msg)
                if 'Cannot get match history' in e.msg:
                    raise e
                if 'Practice matches' in e.msg:
                    raise e
                time.sleep(self.wait)
            except Exception as e:
                self.lock.release()
                self.logger.error(name + ' ' + str(type(e)) + ' ' + str(e.message))
                self.check_tries(tries, e)
                time.sleep(self.wait)

    def get_player_summaries(self, *args):
        name = 'get_player_summaries ' + str(args)
        return self.get_until_success(name, lambda: self.api().get_player_summaries(*args))

    def get_match_history(self, account_id, **kwargs):
        name = 'get_match_history ' + str(account_id) + ' ' + str(kwargs)
        return self.get_until_success(name, lambda: self.api().get_match_history(account_id, **kwargs))

    def get_match_details(self, match_id):
        name = 'get_match_details ' + str(match_id)
        return self.get_until_success(name, lambda: self.api().get_match_details(match_id))

    @staticmethod
    def to_64b(number):
        return dota2api.convert_to_64_bit(number)

    def get_matches_seq(self, last_match_id):
        name = 'get_match_history_by_seq_num ' + str(last_match_id)
        return self.get_until_success(name, lambda: self.api().get_match_history_by_seq_num(last_match_id))

    def get_items(self):
        return self.get_until_success('get_game_items', lambda: self.api().get_game_items())

    def get_heroes(self):
        return self.get_until_success('get_heroes', lambda: self.api().get_heroes())
