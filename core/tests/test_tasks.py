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


class AutoDownloadGamesTest(TestCase):

    def setUp(self):
        self.get_details_match = tasks.get_details_match = mock.Mock()
        self.accounts_to_download_matches = tasks.accounts_to_download_matches = mock.Mock()
        self.last_match_seq = tasks.last_match_seq = mock.Mock()
        self.set_last_match_seq = tasks.set_last_match_seq = mock.Mock()
        self.d2api = tasks.d2api = mock.Mock()
        self.d2api.get_match_history = mock.Mock()
        self.d2api.get_matches_seq = mock.Mock()

    def test_set_last_match_downloaded_if_none_is_downloaded(self):
        self.last_match_seq.return_value = None
        match = build_match_mock(321)

        request = mock.Mock()
        request.matches = [match]

        self.d2api.get_match_history.return_value = request

        self.d2api.get_matches_seq.return_value = request

        tasks._download_by_seq_num()

        self.set_last_match_seq.assert_called_with(321)
        self.d2api.get_match_history.assert_called_with(None)

        self.assertFalse(self.get_details_match.called)

    def test_does_not_download_game_if_there_is_no_interested_player_in_it(self):
        self.last_match_seq.return_value = 0
        self.accounts_to_download_matches.return_value = [9]

        match0 = build_match_mock(4, [3])
        match1 = build_match_mock(5, [1])

        request = mock.Mock()
        request.matches = [match0, match1]

        self.d2api.get_matches_seq.return_value = request

        tasks._download_by_seq_num()

        self.d2api.get_matches_seq.assert_called_with(0)
        self.set_last_match_seq.assert_called_with(5)
        self.assertFalse(self.get_details_match.called)

    def test_do_download_game_if_there_is_interested_player_in_it(self):
        self.last_match_seq.return_value = 1
        self.accounts_to_download_matches.return_value = [9]

        match0 = build_match_mock(1)
        match1 = build_match_mock(4, [9])
        match2 = build_match_mock(5)

        request = mock.Mock()
        request.matches = [match0, match1, match2]

        self.d2api.get_matches_seq.return_value = request

        tasks._download_by_seq_num()

        self.d2api.get_matches_seq.assert_called_with(1)
        self.set_last_match_seq.assert_called_with(5)
        self.get_details_match.assert_called_with(4)


class DefineSkillTest(TestCase):

    def setUp(self):
        self.get_matches_of_skill = tasks.d2api.get_matches_of_skill = mock.Mock()

    def test_define_skill(self):
        request = mock.Mock()
        request.matches = [build_match_mock(22)]

        self.get_matches_of_skill.return_value = request

        tasks._define_skill_match(build_match_mock(22, [44, 55]))

        self.get_matches_of_skill.assert_called_with(22, skill=1, matches_requested=1, hero_id=44)


def build_match_mock(match_id=None, players_accounts_ids=[]):
    class MockList(list):
        pass

    match = mock.Mock()
    match.match_id = match_id
    match.match_seq_num = match_id
    match.players = MockList()

    for account_id in players_accounts_ids:
        player = mock.Mock()
        player.account_id = account_id

        hero = mock.Mock()
        hero.hero_id = account_id

        player.hero = hero

        match.players.append(player)

    match.players.all = lambda: match.players

    return match

