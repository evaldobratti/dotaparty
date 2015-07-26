from django.db import transaction
import utils
from huey.djhuey import crontab, periodic_task, db_task
import logging
import models

log = logging.getLogger('pwm_logger')


@db_task()
def download_games(account_id):
    log.info("requisitando download de " + str(account_id))
    last_match_id = None
    count_hits = 0
    while True:
        try:
            log.info("acc: {} last match: {}".format(account_id, last_match_id or 'started'))
            matches = utils.get_until_success(lambda: utils.d2api.get_match_history(account_id,
                                                                                    start_at_match_id=last_match_id))
            log.info("acc: {} results remaining: {}".format(account_id, matches.results_remaining))
            if matches.results_remaining <= 0:
                log.info("acc: {} finished parsing".format(account_id))
                return

            for match in matches.matches:
                log.info("acc: {} parsing: {}".format(account_id, last_match_id))
                exist = bool(models.DetailMatch.objects.filter(match_id=match.match_id))
                if exist:
                    log.info("acc: {} already parsed: {}".format(account_id, match.match_id))
                    count_hits += 1
                else:
                    with transaction.atomic():
                        utils.get_details_match(match.match_id)
                    log.info("acc: {} parsed: {}".format(account_id, last_match_id))

                last_match_id = match.match_id

        except Exception, e:
            log.exception(e)
