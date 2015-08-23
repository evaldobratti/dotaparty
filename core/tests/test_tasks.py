from django.test import TestCase
from core import tasks
import mock


@mock.patch('core.tasks.d2api')
@mock.patch('core.tasks.get_details_match')
@mock.patch('core.tasks.exists_match')
class DownloadGamesFromUserTest(TestCase):
    def setUp(self):
        pass

    def test_should_not_download_game_if_there_is_no_game(self, exists_match, get_details_match, d2api):
        r = mock.Mock()
        r.results_remaining = 0

        d2api.get_match_history.return_value = r

        tasks._download_games(1)

        self.assertFalse(get_details_match.called, 'Should not download any game.')
        d2api.get_match_history.assert_called_with(1, start_at_match_id=None)

    def test_should_download_games_if_there_is(self, exists_match, get_details_match, d2api):
        match = mock.Mock()
        match.match_id = 321

        first_request = mock.Mock()
        first_request.results_remaining = 1
        first_request.matches = [match]

        second_request = mock.Mock()
        second_request.results_remaining = 0
        second_request.matches = []

        exists_match.return_value = False
        d2api.get_match_history.side_effect = [first_request, second_request]

        tasks._download_games(1)

        get_details_match.assert_called_with(321)

        self.assertEqual(mock.call(1, start_at_match_id=None), d2api.get_match_history.call_args_list[0])
        self.assertEqual(mock.call(1, start_at_match_id=321), d2api.get_match_history.call_args_list[1])


@mock.patch('core.tasks.get_details_match')
@mock.patch('core.tasks.accounts_to_download_matches')
@mock.patch('core.tasks.last_match_of_skill')
@mock.patch('core.tasks.set_last_match_of_skill')
@mock.patch('core.tasks.d2api')
class AutoDownloadGamesTest(TestCase):
    def test_set_last_match_downloaded_if_none_is_downloaded(self, d2api, set_last_match_of_skill, last_match_of_skill, accounts_to_download_matches, get_details_match):
        last_match_of_skill.return_value = None

        match = mock.Mock()
        match.match_id = 321

        request = mock.Mock()
        request.matches = [match]

        d2api.get_matches_of_skill.return_value = request

        tasks._download_games_skill(0)

        set_last_match_of_skill.assert_called_with(0, 321)
        self.assertFalse(get_details_match.called)

    def test_does_not_download_game_if_there_is_no_interested_player_in_it(self, d2api, set_last_match_of_skill, last_match_of_skill, accounts_to_download_matches, get_details_match):
        last_match_of_skill.return_value = 0
        accounts_to_download_matches.return_value = [9]

        match1 = build_match_mock(4, [1])
        match0 = build_match_mock(0)

        request = mock.Mock()
        request.matches = [match1, match0]

        d2api.get_matches_of_skill.return_value = request

        tasks._download_games_skill(0)

        set_last_match_of_skill.assert_called_with(0, 4)
        self.assertFalse(get_details_match.called)

    def test_do_download_game_if_there_is_interested_player_in_it(self, d2api, set_last_match_of_skill, last_match_of_skill, accounts_to_download_matches, get_details_match):
        last_match_of_skill.return_value = 0
        accounts_to_download_matches.return_value = [9]

        match1 = build_match_mock(4, [9])
        match0 = build_match_mock(0)

        request = mock.Mock()
        request.matches = [match1, match0]

        d2api.get_matches_of_skill.return_value = request

        tasks._download_games_skill(0)

        set_last_match_of_skill.assert_called_with(0, 4)
        get_details_match.assert_called_with(4)


def build_match_mock(match_id=None, players_accounts_ids=[]):
    match = mock.Mock()
    match.match_id = match_id
    match.players = []

    for account_id in players_accounts_ids:
        player = mock.Mock()
        player.account_id = account_id

        match.players.append(player)

    return match
