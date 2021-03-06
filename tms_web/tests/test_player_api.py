from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APITestCase
from django.urls import reverse

from tms_web.models import Player
from tms_web.tests.test_team_api import TeamAPITest
import tms_web.constants as constants


class PlayerAPITest(APITestCase):

    @staticmethod
    def create_test_player():
        team = TeamAPITest.create_test_team()
        return baker.make(Player, name='David', team=team, height=185, average_score=3)

    def setUp(self):
        self.user = User.objects.create_user(username='matific', email='matific@tms.com', password='pwd')
        self.client.force_login(user=self.user)

    def assert_player_response(self, resp_data, player=None, data=None):
        self.assertIsNotNone(resp_data)
        self.assertIsNotNone(resp_data['id'])
        self.assertIsNotNone(resp_data['average_score'])
        self.assertIsNotNone(resp_data['height'])
        if data is not None:
            self.assertEqual(resp_data['name'], data['name'])
        else:
            self.assertEqual(resp_data['id'], player.id)
            self.assertEqual(resp_data['name'], player.name)
            self.assertEqual(resp_data['team'], player.team.id)
            self.assertEqual(resp_data['team_name'], player.team.name)

    def test_player_get(self):
        player = PlayerAPITest.create_test_player()
        resp = self.client.get(reverse(constants.PLAYER_URL_NAME, args=[player.id]))
        self.assertEqual(resp.status_code, 200)
        self.assert_player_response(resp_data=resp.data, player=player)

    def test_player_get_without_auth(self):
        player = PlayerAPITest.create_test_player()
        self.client.logout()
        resp = self.client.get(reverse(constants.PLAYER_URL_NAME, args=[player.id]))
        self.assertEqual(resp.status_code, 403)

    def test_get_player_list(self):
        player1 = PlayerAPITest.create_test_player()
        player2 = PlayerAPITest.create_test_player()
        resp = self.client.get(reverse(constants.PLAYERS_URL_NAME))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(resp.data['count'], 2)
        self.assertIsNotNone(resp.data['results'])
        self.assert_player_response(resp_data=resp.data['results'][0], player=player1)
        self.assert_player_response(resp_data=resp.data['results'][1], player=player2)

    def test_player_create(self):
        team = TeamAPITest.create_test_team()
        data = {'name': 'David', 'team': team.id, 'height': 185}
        resp = self.client.post(reverse(constants.PLAYERS_URL_NAME), data=data)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(resp.status_code, 201)
        self.assert_player_response(resp_data=resp.data, data=data)

    def test_player_create_without_auth(self):
        team = TeamAPITest.create_test_team()
        data = {'name': 'David', 'team': team.id, 'height': 185}
        self.client.logout()
        resp = self.client.post(reverse(constants.PLAYERS_URL_NAME), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_player_create_without_team(self):
        data = {'name': 'David', 'height': 185}
        resp = self.client.post(reverse(constants.PLAYERS_URL_NAME), data=data)
        self.assertEqual(Player.objects.count(), 0)
        self.assertEqual(resp.status_code, 400)

    def test_player_create_with_non_existing_team(self):
        data = {'name': 'David', 'team': 477, 'height': 185}
        resp = self.client.post(reverse(constants.PLAYERS_URL_NAME), data=data)
        self.assertEqual(Player.objects.count(), 0)
        self.assertEqual(resp.status_code, 400)

    def test_player_update(self):
        player = PlayerAPITest.create_test_player()
        new_name = 'Ross'
        new_height = 175.00
        data = {'id': player.id, 'name': new_name, 'team': player.team.id, 'height': new_height}
        resp = self.client.put(reverse(constants.PLAYER_URL_NAME, args=[player.id]), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(float(resp.data['height']), new_height)
        self.assert_player_response(resp_data=resp.data, data=data)

    def test_player_update_without_auth(self):
        player = PlayerAPITest.create_test_player()
        new_name = 'Ross'
        data = {'id': player.id, 'name': new_name, 'team': player.team.name, 'height': 175}
        self.client.logout()
        resp = self.client.put(reverse(constants.PLAYER_URL_NAME, args=[player.id]), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_player_update_with_non_existing_team(self):
        player = PlayerAPITest.create_test_player()
        new_name = 'Ross'
        data = {'id': player.id, 'name': new_name, 'team': 133, 'height': 175}
        resp = self.client.put(reverse(constants.PLAYER_URL_NAME, args=[player.id]), data=data)
        self.assertEqual(resp.status_code, 400)

    def test_player_partial_update(self):
        player = PlayerAPITest.create_test_player()
        new_name = 'Mann'
        data = {'name': new_name}
        resp = self.client.patch(reverse(constants.PLAYER_URL_NAME, args=[player.id]), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(resp.data['id'], player.id)
        self.assertEqual(resp.data['name'], new_name)

    def test_player_partial_update_without_auth(self):
        player = PlayerAPITest.create_test_player()
        new_name = 'Mann'
        data = {'name': new_name}
        self.client.logout()
        resp = self.client.patch(reverse(constants.PLAYER_URL_NAME, args=[player.id]), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_player_delete(self):
        player = PlayerAPITest.create_test_player()
        resp = self.client.delete(reverse(constants.PLAYER_URL_NAME, args=[player.id]))
        self.assertEqual(resp.status_code, 204)

    def test_player_delete_without_auth(self):
        player = PlayerAPITest.create_test_player()
        self.client.logout()
        resp = self.client.delete(reverse(constants.PLAYER_URL_NAME, args=[player.id]))
        self.assertEqual(resp.status_code, 403)
