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
last_match_of_skill = utils.last_match_of_skill
set_last_match_of_skill = utils.set_last_match_of_skill


@db_task()
def download_games(account_id):
    _download_games(account_id)


def always_execute(x):
    return True


@db_task()
def download_by_seq_num():
    _download_games_skill()


@db_periodic_task(always_execute)
def games_skill_setter():
    matches = models.DetailMatch.objects.filter(skill__isnull=True)
    for match in matches:
        _define_skill_match(match)


def _define_skill_match(match):
    log.info("match: {} will be ranked".format(match.match_id))
    for player in match.players.all():
        if _define_if_skill(match, player.hero(), 1):
            return
        elif _define_if_skill(match, player.hero(), 2):
            return
        elif _define_if_skill(match, player.hero(), 3):
            return

    log.info("match: {} skill not determined".format(match.match_id))
    match.skill = 4
    match.save()

def _define_if_skill(match, hero, skill_lvl):
    skill = d2api.get_matches_of_skill(match.match_id,
                                       skill=skill_lvl,
                                       matches_requested=1,
                                       hero_id=hero.hero_id)

    if skill.matches and skill.matches[0].match_id == match.match_id:
        log.info("match: {} skill: {}".format(match.match_id, skill_lvl))
        match.skill = skill_lvl
        match.save()
        return True

    return False


def _download_games_skill():
    last_match_seq_num = 1552584004
    while True:
        try:
            matches = d2api.get_matches_seq(last_match_seq_num)
            for match in matches.matches:
                log.info("analysing match_id : {} seq_num: {}".format(match.match_id, match.match_seq_num))

                accs = accounts_to_download_matches()

                log.info("match_id : {} seq_num: {} accs in match: {} ".format(match.match_id, match.match_seq_num,
                                                                               [p.account_id for p in match.players]))
                if [p for p in match.players if p.account_id in accs]:
                    log.info("will download match_id : {} seq_num: {}".format(match.match_id, match.match_seq_num))
                    match = _download_match('worker on downloads', match)
                else:
                    log.info("match_id : {} not downloaded!".format(match.match_id))

                last_match_seq_num = match.match_seq_num
        except Exception, e:
            log.exception(e)


def _download_games(account_id):
    log.info("requisitando download de " + str(account_id))
    last_match_id = None
    while True:
        try:
            log.info("acc: {} last match: {}".format(account_id, last_match_id or 'started'))
            matches = d2api.get_match_history(account_id,
                                              start_at_match_id=last_match_id)
            log.info("acc: {} results remaining: {}".format(account_id, matches.results_remaining))

            if matches.results_remaining <= 0:
                log.info("acc: {} finished parsing".format(account_id))
                return

            for match in matches.matches:
                _download_match(account_id, match)

                last_match_id = match.match_id

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
