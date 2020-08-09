from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APITestCase
from django.urls import reverse

from tms_web.models import Match, Team, MatchTeam, Player, MatchPlayer
import tms_web.constants as constants
from tms_web.tests.test_team_api import TeamAPITest


class MatchAPITest(APITestCase):

    _MATCHES_API_NAME = constants.MATCHES_URL_NAME + '-list'
    _MATCH_API_NAME = constants.MATCHES_URL_NAME + '-detail'
    _MATCH_TEAMS_API_NAME = constants.MATCHES_URL_NAME + '-' + constants.MATCH_TEAMS_URL_NAME
    _MATCH_PLAYERS_API_NAME = constants.MATCHES_URL_NAME + '-' + constants.MATCH_PLAYERS_URL_NAME

    @staticmethod
    def create_test_match():
        team1 = TeamAPITest.create_test_team()
        team2 = TeamAPITest.create_test_team()
        return baker.make(Match, round=Match.QUALIFYING, team1_score=5, team2_score=3, team1=team1, team2=team2)

    def setUp(self):
        self.user = User.objects.create_user(username='matific', email='matific@tms.com', password='pwd')
        self.client.force_login(user=self.user)

    def assert_match_response(self, resp_data, match=None, data=None):
        self.assertIsNotNone(resp_data)
        self.assertIsNotNone(resp_data['id'])
        self.assertIsNotNone(resp_data['scheduled_date'])
        self.assertIsNotNone(resp_data['stadium'])
        self.assertIsNotNone(resp_data['round'])
        self.assertIsNotNone(resp_data['team1'])
        self.assertIsNotNone(resp_data['team2'])
        self.assertIsNotNone(resp_data['team1_score'])
        self.assertIsNotNone(resp_data['team2_score'])
        if data is not None:
            self.assertEqual(resp_data['stadium'], data['stadium'])
            self.assertEqual(resp_data['round'], data['round'])
            self.assertEqual(resp_data['team1'], data['team1'])
            self.assertEqual(resp_data['team2'], data['team2'])
            self.assertEqual(resp_data['team1_score'], data['team1_score'])
            self.assertEqual(resp_data['team2_score'], data['team2_score'])
        else:
            self.assertEqual(resp_data['id'], match.id)
            self.assertEqual(resp_data['stadium'], match.stadium)
            self.assertEqual(resp_data['round'], match.round)
            self.assertEqual(resp_data['team1'], match.team1.id)
            self.assertEqual(resp_data['team2'], match.team2.id)
            self.assertEqual(resp_data['team1_score'], match.team1_score)
            self.assertEqual(resp_data['team2_score'], match.team2_score)

    def _get_match_data(self):
        team1 = baker.make(Team, name='Brazil')
        team2 = baker.make(Team, name='USA')
        return {'scheduled_date': '2020-08-31', 'stadium': 'Dallas', 'round': Match.QUALIFYING, 'team1': team1.id,
                'team2': team2.id, 'team1_score': 3, 'team2_score': 5}

    def test_match_get(self):
        match = MatchAPITest.create_test_match()
        resp = self.client.get(reverse(MatchAPITest._MATCH_API_NAME, args=[match.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(resp.data['id'], match.id)
        self.assert_match_response(resp_data=resp.data, match=match)

    def test_match_get_without_auth(self):
        match = MatchAPITest.create_test_match()
        self.client.logout()
        resp = self.client.get(reverse(MatchAPITest._MATCH_API_NAME, args=[match.id]))
        self.assertEqual(resp.status_code, 403)

    def test_get_match_list(self):
        match = MatchAPITest.create_test_match()
        resp = self.client.get(reverse(MatchAPITest._MATCHES_API_NAME))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(resp.data['count'], 1)
        self.assertIsNotNone(resp.data['results'])
        self.assert_match_response(resp_data=resp.data['results'][0], match=match)

    def test_get_match_list_without_auth(self):
        self.client.logout()
        resp = self.client.get(reverse(MatchAPITest._MATCHES_API_NAME))
        self.assertEqual(resp.status_code, 403)

    def test_match_create(self):
        data = self._get_match_data()
        resp = self.client.post(reverse(MatchAPITest._MATCHES_API_NAME), data=data)
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(resp.status_code, 201)
        self.assert_match_response(resp_data=resp.data, data=data)
        match_id = resp.data['id']
        self.assertIsNotNone(match_id)
        self.assertEqual(len(MatchTeam.objects.all().filter(match=match_id)), 2)

    def test_match_create_without_auth(self):
        self.client.logout()
        resp = self.client.post(reverse(MatchAPITest._MATCHES_API_NAME), data=self._get_match_data())
        self.assertEqual(resp.status_code, 403)

    def test_match_delete(self):
        match = MatchAPITest.create_test_match()
        resp = self.client.delete(reverse(MatchAPITest._MATCH_API_NAME, args=[match.id]))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Match.objects.count(), 0)
        self.assertEqual(len(MatchTeam.objects.all().filter(match=match.id)), 0)

    def test_match_delete_without_auth(self):
        match = MatchAPITest.create_test_match()
        self.client.logout()
        resp = self.client.delete(reverse(MatchAPITest._MATCH_API_NAME, args=[match.id]))
        self.assertEqual(resp.status_code, 403)

    def test_match_players_get(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        player = baker.make(Player, team=team)
        baker.make(MatchPlayer, player=player, match=match, score=4)
        resp = self.client.get(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[match.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)

    def test_match_players_get_without_auth(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        player = baker.make(Player, team=team)
        baker.make(MatchPlayer, player=player, match=match, score=4)
        self.client.logout()
        resp = self.client.get(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[match.id]))
        self.assertEqual(resp.status_code, 403)

    def test_match_player_create(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        player = baker.make(Player, team=team)
        data = {'match': match.id, 'player': player.id, 'score': 4}
        resp = self.client.post(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[match.id]), data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertIsNotNone(resp.data)
        self.assertEqual(MatchPlayer.objects.count(), 1)
        self.assertEqual(Player.objects.get(id=player.id).average_score, 4)
        self.assertEqual(Player.objects.get(id=player.id).matches, 1)

    def test_match_player_create_without_auth(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        data = {'match': match.id, 'team': team.name, 'score': 4}
        self.client.logout()
        resp = self.client.post(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[match.id]), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_match_player_update(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        player = baker.make(Player, team=team)
        baker.make(MatchPlayer, player=player, match=match)
        data = {'match': match.id, 'player': player.id, 'score': 4}
        resp = self.client.put(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[match.id]), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(Player.objects.get(id=player.id).average_score, 4)
        self.assertEqual(Player.objects.get(id=player.id).matches, 1)

    def test_match_player_update_without_auth(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        player = baker.make(Player, team=team)
        baker.make(MatchPlayer, player=player, match=match)
        data = {'match': match.id, 'player': player.id, 'score': 4}
        self.client.logout()
        resp = self.client.put(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[match.id]), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_match_player_update_non_existing_player(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        player = baker.make(Player, team=team)
        baker.make(MatchPlayer, player=player, match=match)
        data = {'match': match.id, 'player': 2, 'score': 4}
        resp = self.client.put(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[match.id]), data=data)
        self.assertEqual(resp.status_code, 404)

    def test_match_player_update_non_existing_match(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        player = baker.make(Player, team=team)
        baker.make(MatchPlayer, player=player, match=match)
        data = {'match': 455, 'player': player.id, 'score': 4}
        resp = self.client.put(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[match.id]), data=data)
        self.assertEqual(resp.status_code, 400)

    def test_match_player_update_non_existing_match_in_path(self):
        match = MatchAPITest.create_test_match()
        team = baker.make(Team, name='Brazil', average_score=0)
        player = baker.make(Player, team=team)
        baker.make(MatchPlayer, player=player, match=match)
        data = {'match': match.id, 'player': player.id, 'score': 4}
        resp = self.client.put(reverse(MatchAPITest._MATCH_PLAYERS_API_NAME, args=[444]), data=data)
        self.assertEqual(resp.status_code, 404)
