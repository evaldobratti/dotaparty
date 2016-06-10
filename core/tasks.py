from huey.djhuey import db_task
from django.db import transaction
from core import d2api
from core import utils
import logging
import models

log = logging.getLogger('dotaparty.tasks')


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
                                                                         matches['results_remaining']))

                for match in matches['matches']:
                    schedule_download_match(match['match_id'], False)

                    last_match_id = match['match_id']

                if matches['results_remaining'] <= 0:
                    last_match_id = None
                    log.info("acc: {} finished parsing hero {}".format(account.account_id, hero.localized_name))
                    if hero.localized_name.lower().startswith('z'):
                        log.info("acc: {} finished parsing ALL".format(account.account_id))
                        account.matches_download_required = True
                        account.save()
                        return

            except Exception, e:
                log.exception(e)


def define_if_skill(match, hero_id, skill_lvl):
    skill = d2api.get_match_history(None, start_at_match_id=match.match_id,
                                    skill=skill_lvl,
                                    matches_requested=5,
                                    hero_id=hero_id)

    if skill['matches']:
        for m in skill['matches']:
            if m['match_id'] == match.match_id:
                log.info("match: {} IS skill: {}".format(match.match_id, skill_lvl))
                match.skill = skill_lvl
                match.save()
                return True

    log.info("match: {} is NOT skill: {}".format(match.match_id, skill_lvl))
    return False


@db_task()
def schedule_determine_skill(match_id, player_index=0, skill=1):
    match = models.DetailMatch.objects.get(match_id=match_id)

    player = match.players.order_by('player_slot')[player_index]
    log.info("match: {} will be ranked with {} {}".format(match.match_id, player.hero.localized_name, skill))
    if not define_if_skill(match, player.hero.hero_id, skill):
        if skill < 3:
            schedule_determine_skill(match.match_id, player_index, skill + 1)
        elif player_index < 9:
            schedule_determine_skill(match.match_id, player_index + 1, 1)
        else:
            log.info("match: {} skill not determined".format(match.match_id))
            match.skill = 4
            match.save()


@db_task(retries=3)
def schedule_download_match(match_id, set_skill):
    download_match(match_id, set_skill)


def download_match(match_id, set_skill):
    log.info("parsing: {}".format(match_id))
    exist = models.DetailMatch.objects.filter(match_id=match_id)
    if exist:
        log.info("already parsed, skipping: {}".format(match_id))
        return exist[0]
    else:
        with transaction.atomic():
            match = utils.get_details_match(match_id)

        if set_skill:
            schedule_determine_skill(match.match_id)
        else:
            match.skill = 4
            match.save()
        log.info("parsed: {}".format(match.match_id))
        return match
