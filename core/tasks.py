from django.db import transaction
import utils
from huey.djhuey import db_task, db_periodic_task, crontab
import logging
import models

log = logging.getLogger('pwm_logger')

d2api = utils.d2api
get_details_match = utils.get_details_match
exists_match = models.DetailMatch.objects.filter

accounts_to_download_matches = utils.accounts_to_download_matches
last_match_seq = utils.last_match_seq
set_last_match_seq = utils.set_last_match_seq


@db_task()
def download_games(account_id):
    _download_games(account_id)


def always_execute(x):
    return True


@db_task()
def download_by_seq_num():
    _download_by_seq_num()


@db_task()
def games_skill_setter():
    while True:
        import time
        time.sleep(30)
        matches = models.DetailMatch.objects.filter(skill__isnull=True)
        log.info("matches to set skill: {} ".format(len(matches)))
        for match in matches:
            _define_skill_match(match)


def _define_skill_match(match):
    log.info("match: {} will be ranked".format(match.match_id))
    for player in match.players.all():
        if _define_if_skill(match, player.hero, 1):
            return
        elif _define_if_skill(match, player.hero, 2):
            return
        elif _define_if_skill(match, player.hero, 3):
            return

    log.info("match: {} skill not determined".format(match.match_id))
    match.skill = 4
    match.save()


def _define_if_skill(match, hero, skill_lvl):
    skill = d2api.get_match_history(None, start_at_match_id=match.match_id,
                                    skill=skill_lvl,
                                    matches_requested=1,
                                    hero_id=hero.hero_id)

    if skill.matches and skill.matches[0].match_id == match.match_id:
        log.info("match: {} IS skill: {}".format(match.match_id, skill_lvl))
        match.skill = skill_lvl
        match.save()
        return True

    log.info("match: {} is NOT skill: {}".format(match.match_id, skill_lvl))
    return False

def _download_by_seq_num():
    while True:
        last_match_seq_num = last_match_seq()

        if last_match_seq_num is None:
            set_last_match_seq(d2api.get_match_history(None).matches[0].match_seq_num)
            last_match_seq_num = last_match_seq()

        try:
            matches = d2api.get_matches_seq(last_match_seq_num)
            for match in matches.matches:
                log.info("analysing match_id : {} seq_num: {}".format(match.match_id, match.match_seq_num))

                accs = accounts_to_download_matches()

                if [p for p in match.players if p.account_id in accs]:
                    log.info("will download match_id : {} seq_num: {}".format(match.match_id, match.match_seq_num))
                    match = _download_match('worker on downloads', match)

                set_last_match_seq(match.match_seq_num)
        except Exception, e:
            log.exception(e)


def _download_games(account_id):
    log.info("requisitando download de " + str(account_id))
    last_match_id = None
    heroes = models.Hero.objects.all().order_by('localized_name')
    while True:
        for hero in heroes:
            try:
                log.info("acc: {} hero: {} last match: {}".format(account_id, hero.localized_name,
                                                                  last_match_id or 'started'))
                matches = d2api.get_match_history(account_id,
                                                  start_at_match_id=last_match_id,
                                                  hero_id=hero.hero_id)
                log.info("acc: {} hero: {} results remaining: {}".format(account_id, hero.localized_name,
                                                                         matches.results_remaining))

                for match in matches.matches:
                    _download_match(account_id, match)

                    last_match_id = match.match_id

                if matches.results_remaining <= 0:
                    last_match_id = None
                    log.info("acc: {} finished parsing hero {}".format(account_id, hero.localized_name))
                    if hero == heroes.reverse()[0]:
                        log.info("acc: {} finished parsing ALL".format(account_id))
                        return

            except Exception, e:
                log.exception(e)


def _download_match(account_id, match):
    log.info("acc: {} parsing: {}".format(account_id, match.match_id))
    exist = exists_match(match_id=match.match_id)
    if exist:
        log.info("acc: {} already parsed: {}".format(account_id, match.match_id))
        return exist[0]
    else:
        with transaction.atomic():
            match = get_details_match(match.match_id)
        log.info("acc: {} parsed: {}".format(account_id, match.match_id))
        return match
