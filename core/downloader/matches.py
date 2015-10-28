from django.db import transaction
from core import d2api
from core import utils
from core import models
from core.parameters import INTERESTED_ACCOUNTS_IDS
from core.parameters import LAST_MATCH_SEQ_NUM

import logging

log = logging.getLogger('DownloaderGamesBySeqNum')


def download_match(message, match):
    log.info("from: {} parsing: {}".format(message, match.match_id))
    exist = models.DetailMatch.objects.filter(match_id=match.match_id)
    if exist:
        log.info("from: {} already parsed: {}".format(message, match.match_id))
        return exist[0]
    else:
        with transaction.atomic():
            match = utils.get_details_match(match.match_id)
        log.info("from: {} parsed: {}".format(message, match.match_id))
        return match


class DownloaderGamesBySeqNum(object):

    def execute(self):
        while True:
            last_match_seq_num = self.__get_last_match_seq_num()

            try:
                matches = d2api.get_matches_seq(last_match_seq_num)
                for match in matches.matches:
                    self.__download_match_if_interested(match)
                    LAST_MATCH_SEQ_NUM.set_value(match.match_seq_num)
            except Exception, e:
                log.exception(e)

    @staticmethod
    def __download_match_if_interested(match):
        log.info("analysing match_id : {} seq_num: {}".format(match.match_id, match.match_seq_num))

        if [p for p in match.players if p.account_id in INTERESTED_ACCOUNTS_IDS.value()]:
            log.info("will download match_id : {} seq_num: {}".format(match.match_id, match.match_seq_num))
            download_match('worker on downloads', match)

    @staticmethod
    def __get_last_match_seq_num():
        last_match_seq_num = LAST_MATCH_SEQ_NUM.value()
        if last_match_seq_num is None:
            LAST_MATCH_SEQ_NUM.set_value(d2api.get_match_history(None).matches[0].match_seq_num)
            last_match_seq_num = LAST_MATCH_SEQ_NUM.value()
        return last_match_seq_num


def execute_download_games():
    DownloaderGamesBySeqNum().execute()
