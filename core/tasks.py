from django.db import transaction
import utils
from huey.djhuey import db_task, db_periodic_task
import logging
import models
import itertools

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


@db_periodic_task(always_execute)
def download_matches_skill_very_high():
    _download_games_skill(3)


@db_periodic_task(always_execute)
def download_matches_skill_high():
    _download_games_skill(2)


@db_periodic_task(always_execute)
def download_matches_skill_normal():
    _download_games_skill(1)


#
#
# @db_periodic_task(always_execute)
# def download_matches_skill_undefined():
#     _download_games_skill(0)


def _download_games_skill(skill):
    last_match_hero_downloaded = {}

    heroes = models.Hero.objects.all()

    for hero in itertools.cycle(heroes):
        last_match = last_match_hero_downloaded.get(hero)
        if last_match is None:
            try:
                matches = d2api.get_matches_of_skill(None, skill, hero.hero_id)
                log.info("no game downloaded of skill: {} hero: {} setting to: {}".format(skill, hero.localized_name,
                                                                                          matches.matches[0].match_id))
                last_match_hero_downloaded[hero] = matches.matches[0].match_id
            except Exception, e:
                log.info("skill: {} hero: {} error: {}", skill, hero.hero_id, e.message)
                log.exception(e)
        else:
            first_downloaded = None
            last_match_id = None
            while True:
                should_break = False
                try:
                    matches = d2api.get_matches_of_skill(last_match_id, skill, hero.hero_id)
                    for match in matches.matches:
                        log.info("skill: {} hero: {} analysing match_id : {}".format(skill, hero.localized_name,
                                                                                     match.match_id))
                        if not first_downloaded:
                            first_downloaded = match.match_id

                        accs = accounts_to_download_matches()

                        log.info("skill: {} hero: {} accs in match: {}".format(skill, hero.localized_name,
                                                                               [p.account_id for p in match.players]))
                        if [p for p in match.players if p.account_id in accs]:
                            log.info("skill: {} will download match_id : {}".format(skill, match.match_id))
                            match = _download_match('Worker on skill ' + str(skill), match)
                            match.skill = skill
                            match.save()
                        else:
                            log.info(
                                "skill: {} hero: {} match_id : {} not downloaded!".format(skill, hero.localized_name,
                                                                                          match.match_id))

                        if last_match == match.match_id:
                            log.info(
                                "skill: {} hero: {} updating last match match_id : {}".format(skill,
                                                                                              hero.localized_name,
                                                                                              first_downloaded))
                            last_match_hero_downloaded[hero] = first_downloaded
                            should_break = True
                            break

                        last_match_id = match.match_id

                    if should_break:
                        break
                except Exception, e:
                    log.info("skill: {} hero: {} error: {}", skill, hero.hero_id, e.message)
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
