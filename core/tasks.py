from huey.djhuey import db_task
from core import d2api
from core.downloader.matches import download_match
import logging
import models

log = log = logging.getLogger('DownloaderByPlayer')


@db_task()
def download_games(account_id):
    _download_games(account_id)


def _download_games(account):
    log.info("requiring download de " + str(account.account_id))
    account = models.Account.objects.get(account_id=int(account.account_id))
    if account.matches_download_required:
        log.info("all matches already downloaded " + str(account.account_id))
        return

    last_match_id = None
    heroes = models.Hero.objects.all().order_by('localized_name')
    while True:
        for hero in heroes:
            try:
                log.info("acc: {} hero: {} last match: {}".format(account.account_id, hero.localized_name,
                                                                  last_match_id or 'started'))
                matches = d2api.get_match_history(account.account_id,
                                                  start_at_match_id=last_match_id,
                                                  hero_id=hero.hero_id)
                log.info("acc: {} hero: {} results remaining: {}".format(account.account_id, hero.localized_name,
                                                                         matches.results_remaining))

                for match in matches.matches:
                    detail_match = download_match(account.account_id, match)
                    detail_match.skill = 4
                    detail_match.save()

                    last_match_id = match.match_id

                if matches.results_remaining <= 0:
                    last_match_id = None
                    log.info("acc: {} finished parsing hero {}".format(account.account_id, hero.localized_name))
                    if hero == heroes.reverse()[0]:
                        log.info("acc: {} finished parsing ALL".format(account.account_id))
                        return

            except Exception, e:
                log.exception(e)



