from django.db import transaction
from core import d2api
from core import utils
from core import models
from core import tasks
from core.parameters import INTERESTED_ACCOUNTS_IDS
from core.parameters import LAST_MATCH_SEQ_NUM
from huey.djhuey import db_task

import logging
LOGGER = logging.getLogger('dotaparty.downloader')

d2api.logger = LOGGER


class DownloaderGamesBySeqNum(object):

    def execute(self):
        while True:
            last_match_seq_num = self.__get_last_match_seq_num()
            try:
                matches = d2api.get_matches_seq(last_match_seq_num)
                for match in matches['matches']:
                    accounts_ids = [p.get('account_id') for p in match['players'] if p.get('account_id', -1)]
                    tasks.download_match_if_interested(match['match_id'], match['match_seq_num'], accounts_ids)
                    LAST_MATCH_SEQ_NUM.set_value(match['match_seq_num'])
                LOGGER.info("last seq num: " + str(last_match_seq_num) + ' matches retrieved: ' + str(len(matches['matches'])))
            except Exception, e:
                print e
                LOGGER.exception(e)
                if e.message == 'Error retrieving match data.' or \
                        (hasattr(e, 'msg') and e.msg == 'Error retrieving match data.'):
                    LAST_MATCH_SEQ_NUM.set_value(long(last_match_seq_num) + 1)

    def __download_match_if_interested(self, match, interested_accounts):
        LOGGER.info("analysing match_id : {} seq_num: {}".format(match['match_id'], match['match_seq_num']))

        accounts_ids = set([p.get('account_id') for p in match['players'] if p.get('account_id', -1)])
        if accounts_ids.intersection(interested_accounts):
            LOGGER.info("will download match_id : {} seq_num: {}".format(match['match_id'], match['match_seq_num']))
            tasks.schedule_download_match(match['match_id'], True)

    def __get_last_match_seq_num(self):
        last_match_seq_num = LAST_MATCH_SEQ_NUM.value()
        if last_match_seq_num is None:
            LAST_MATCH_SEQ_NUM.set_value(d2api.get_match_history(None)['matches'][0]['match_seq_num'])
            last_match_seq_num = LAST_MATCH_SEQ_NUM.value()
        return last_match_seq_num


def execute_download_games():
    DownloaderGamesBySeqNum().execute()
