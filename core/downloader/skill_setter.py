from core import d2api
from core import models
import logging

LOGGER_NAME = 'DownloaderGameSkill'
log = logging.getLogger(LOGGER_NAME)


def _define_if_skill(match, hero, skill_lvl):
    skill = d2api.get_match_history(None, start_at_match_id=match.match_id,
                                    skill=skill_lvl,
                                    matches_requested=1,
                                    hero_id=hero.hero_id)

    if skill['matches'] and skill['matches'][0]['match_id'] == match.match_id:
        log.info("match: {} IS skill: {}".format(match.match_id, skill_lvl))
        match.skill = skill_lvl
        match.save()
        return True

    log.info("match: {} is NOT skill: {}".format(match.match_id, skill_lvl))
    return False


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


def execute_skill_setter():
    while True:
        import time
        time.sleep(30)
        matches = models.DetailMatch.objects.filter(skill__isnull=True)
        log.info("matches to set skill: {} ".format(len(matches)))
        for match in matches:
            _define_skill_match(match)


