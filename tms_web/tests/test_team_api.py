from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APITestCase
from django.urls import reverse

from tms_web.models import Team, Player
import tms_web.constants as constants


class TeamAPITest(APITestCase):

    _TEAMS_API_NAME = constants.TEAMS_URL_NAME + '-list'
    _TEAM_API_NAME = constants.TEAMS_URL_NAME + '-detail'
    _TEAM_TOP_PLAYERS_API_NAME = constants.TEAMS_URL_NAME + '-' + constants.TOP_PLAYERS_URL_SUFFIX
    _TEAM_PLAYERS_API_NAME = constants.TEAMS_URL_NAME + '-' + constants.TEAM_PLAYERS_URL_SUFFIX

    @staticmethod
    def create_test_team():
        return baker.make(Team, name='Brazil', average_score=7)

    def setUp(self):
        self.user = User.objects.create_user(username='matific', email='matific@tms.com', password='pwd')
        self.client.force_login(user=self.user)

    def test_team_create(self):
        data = {'name': 'Sri Lanka'}
        resp = self.client.post(reverse(TeamAPITest._TEAMS_API_NAME), data=data)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(resp.status_code, 201)
        self.assertIsNotNone(resp.data)
        # self.assertIsNotNone(resp.data['id'])

    def test_team_create_without_auth(self):
        data = {'name': 'Sri Lanka'}
        self.client.logout()
        resp = self.client.post(reverse(TeamAPITest._TEAMS_API_NAME), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_team_get(self):
        team = TeamAPITest.create_test_team()
        resp = self.client.get(reverse(TeamAPITest._TEAM_API_NAME, args=[team.name]))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        # self.assertEqual(resp.data['id'], team.id)
        self.assertEqual(resp.data['name'], team.name)

    def test_team_get_without_auth(self):
        team = TeamAPITest.create_test_team()
        self.client.logout()
        resp = self.client.get(reverse(TeamAPITest._TEAM_API_NAME, args=[team.name]))
        self.assertEqual(resp.status_code, 403)

    def test_team_update(self):
        team = TeamAPITest.create_test_team()
        new_name = 'Russia'
        data = {'name': new_name}
        resp = self.client.put(reverse(TeamAPITest._TEAM_API_NAME, args=[team.name]), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        # self.assertEqual(resp.data['id'], team.id)
        self.assertEqual(resp.data['name'], new_name)

    def test_team_update_without_auth(self):
        team = TeamAPITest.create_test_team()
        new_name = 'Russia'
        data = {'name': new_name}
        self.client.logout()
        resp = self.client.put(reverse(TeamAPITest._TEAM_API_NAME, args=[team.name]), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_team_partial_update(self):
        team = TeamAPITest.create_test_team()
        new_name = 'India'
        data = {'name': new_name}
        resp = self.client.patch(reverse(TeamAPITest._TEAM_API_NAME, args=[team.name]), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        # self.assertEqual(resp.data['id'], team.id)
        self.assertEqual(resp.data['name'], new_name)

    def test_team_partial_update_without_auth(self):
        team = TeamAPITest.create_test_team()
        new_name = 'India'
        data = {'name': new_name}
        self.client.logout()
        resp = self.client.patch(reverse(TeamAPITest._TEAM_API_NAME, args=[team.name]), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_team_delete(self):
        team = TeamAPITest.create_test_team()
        resp = self.client.delete(reverse(TeamAPITest._TEAM_API_NAME, args=[team.name]))
        self.assertEqual(resp.status_code, 204)

    def test_team_delete_without_auth(self):
        team = TeamAPITest.create_test_team()
        self.client.logout()
        resp = self.client.delete(reverse(TeamAPITest._TEAM_API_NAME, args=[team.name]))
        self.assertEqual(resp.status_code, 403)

    def test_top_player(self):
        team = TeamAPITest.create_test_team()
        baker.make(Player, team=team, average_score=9)
        baker.make(Player, team=team, average_score=10)
        baker.make(Player, team=team, average_score=1)
        baker.make(Player, team=team, average_score=5)
        baker.make(Player, team=team, average_score=8)
        resp = self.client.get(reverse(TeamAPITest._TEAM_TOP_PLAYERS_API_NAME, args=[team.name]))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(len(resp.data), 1)

    def test_team_players(self):
        team = TeamAPITest.create_test_team()
        team1 = baker.make(Team, name='USA', average_score=7)
        baker.make(Player, team=team)
        baker.make(Player, team=team)
        baker.make(Player, team=team)
        baker.make(Player, team=team1)
        resp = self.client.get(reverse(TeamAPITest._TEAM_PLAYERS_API_NAME, args=[team.name]))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(len(resp.data), 3)
