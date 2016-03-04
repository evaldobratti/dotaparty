from django.db import transaction
from core import d2api
from core import utils
from core import models
from core import tasks
from core.parameters import INTERESTED_ACCOUNTS_IDS
from core.parameters import LAST_MATCH_SEQ_NUM

import logging
LOGGER_NAME = 'Downloader'


def get_logger():
    return logging.getLogger(LOGGER_NAME)


class DownloaderGamesBySeqNum(object):

    def execute(self):
        while True:
            last_match_seq_num = self.__get_last_match_seq_num()
            try:
                matches = d2api.get_matches_seq(last_match_seq_num)
                for match in matches['matches']:
                    self.__download_match_if_interested(match)
                    LAST_MATCH_SEQ_NUM.set_value(match['match_seq_num'])
            except Exception, e:
                print e
                get_logger().exception(e)

    def __download_match_if_interested(self, match):
        get_logger().info("analysing match_id : {} seq_num: {}".format(match['match_id'], match['match_seq_num']))

        if [p for p in match['players'] if p.get('account_id', -1) in INTERESTED_ACCOUNTS_IDS.value()]:
            get_logger().info("will download match_id : {} seq_num: {}".format(match['match_id'], match['match_seq_num']))
            tasks.schedule_download_match(match['match_id'], False)

    def __get_last_match_seq_num(self):
        last_match_seq_num = LAST_MATCH_SEQ_NUM.value()
        if last_match_seq_num is None:
            LAST_MATCH_SEQ_NUM.set_value(d2api.get_match_history(None).matches[0].match_seq_num)
            last_match_seq_num = LAST_MATCH_SEQ_NUM.value()
        return last_match_seq_num


def execute_download_games():
    DownloaderGamesBySeqNum().execute()
