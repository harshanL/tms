from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APITestCase
from django.urls import reverse

from tms_web.models import Coach
from tms_web.tests.test_team_api import TeamAPITest
import tms_web.constants as constants


class CoachAPITest(APITestCase):

    @staticmethod
    def create_test_coach():
        team = TeamAPITest.create_test_team()
        return baker.make(Coach, name='David', team=team)

    def setUp(self):
        self.user = User.objects.create_user(username='matific', email='matific@tms.com', password='pwd')
        self.client.force_login(user=self.user)

    def assert_coach_response(self, resp_data, coach=None, data=None):
        self.assertIsNotNone(resp_data)
        if data is not None:
            self.assertIsNotNone(resp_data['id'])
            self.assertEqual(resp_data['name'], data['name'])
            self.assertEqual(resp_data['team'], data['team'])
            self.assertIsNotNone(resp_data['team_name'])
        else:
            self.assertEqual(resp_data['id'], coach.id)
            self.assertEqual(resp_data['name'], coach.name)
            self.assertEqual(resp_data['team'], coach.team.id)
            self.assertEqual(resp_data['team_name'], coach.team.name)

    def test_coach_get(self):
        coach = CoachAPITest.create_test_coach()
        resp = self.client.get(reverse(constants.COACH_URL_NAME, args=[coach.id]))
        self.assertEqual(resp.status_code, 200)
        self.assert_coach_response(resp_data=resp.data, coach=coach)

    def test_coach_get_without_auth(self):
        coach = CoachAPITest.create_test_coach()
        self.client.logout()
        resp = self.client.get(reverse(constants.COACH_URL_NAME, args=[coach.id]))
        self.assertEqual(resp.status_code, 403)

    def test_get_coach_list(self):
        coach1 = CoachAPITest.create_test_coach()
        coach2 = CoachAPITest.create_test_coach()
        resp = self.client.get(reverse(constants.COACHES_URL_NAME))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(resp.data['count'], 2)
        self.assertIsNotNone(resp.data['results'])
        self.assert_coach_response(resp_data=resp.data['results'][0], coach=coach1)
        self.assert_coach_response(resp_data=resp.data['results'][1], coach=coach2)

    def test_coach_create(self):
        team = TeamAPITest.create_test_team()
        data = {'name': 'David', 'team': team.id}
        resp = self.client.post(reverse(constants.COACHES_URL_NAME), data=data)
        self.assertEqual(Coach.objects.count(), 1)
        self.assertEqual(resp.status_code, 201)
        self.assert_coach_response(resp_data=resp.data, data=data)

    def test_coach_create_without_auth(self):
        team = TeamAPITest.create_test_team()
        data = {'name': 'David', 'team': team.name}
        self.client.logout()
        resp = self.client.post(reverse(constants.COACHES_URL_NAME), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_coach_create_without_team(self):
        data = {'name': 'David'}
        resp = self.client.post(reverse(constants.COACHES_URL_NAME), data=data)
        self.assertEqual(Coach.objects.count(), 0)
        self.assertEqual(resp.status_code, 400)

    def test_coach_create_with_non_existing_team(self):
        data = {'name': 'David', 'team': 4}
        resp = self.client.post(reverse(constants.COACHES_URL_NAME), data=data)
        self.assertEqual(Coach.objects.count(), 0)
        self.assertEqual(resp.status_code, 400)

    def test_coach_update(self):
        coach = CoachAPITest.create_test_coach()
        new_name = 'Ross'
        data = {'id': coach.id, 'name': new_name, 'team': coach.team.id}
        resp = self.client.put(reverse(constants.COACH_URL_NAME, args=[coach.id]), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], coach.id)
        self.assert_coach_response(resp_data=resp.data, data=data)

    def test_coach_update_without_auth(self):
        coach = CoachAPITest.create_test_coach()
        new_name = 'Ross'
        data = {'id': coach.id, 'name': new_name, 'team': coach.team.id}
        self.client.logout()
        resp = self.client.put(reverse(constants.COACH_URL_NAME, args=[coach.id]), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_coach_update_with_non_existing_team(self):
        coach = CoachAPITest.create_test_coach()
        new_name = 'Ross'
        data = {'id': coach.id, 'name': new_name, 'team': 3}
        resp = self.client.put(reverse(constants.COACH_URL_NAME, args=[coach.id]), data=data)
        self.assertEqual(resp.status_code, 400)

    def test_coach_partial_update(self):
        coach = CoachAPITest.create_test_coach()
        new_name = 'Mann'
        data = {'name': new_name}
        resp = self.client.patch(reverse(constants.COACH_URL_NAME, args=[coach.id]), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertEqual(resp.data['id'], coach.id)
        self.assertEqual(resp.data['name'], new_name)

    def test_coach_partial_update_without_auth(self):
        coach = CoachAPITest.create_test_coach()
        new_name = 'Mann'
        data = {'name': new_name}
        self.client.logout()
        resp = self.client.patch(reverse(constants.COACH_URL_NAME, args=[coach.id]), data=data)
        self.assertEqual(resp.status_code, 403)

    def test_coach_delete(self):
        coach = CoachAPITest.create_test_coach()
        resp = self.client.delete(reverse(constants.COACH_URL_NAME, args=[coach.id]))
        self.assertEqual(resp.status_code, 204)

    def test_coach_delete_without_auth(self):
        coach = CoachAPITest.create_test_coach()
        self.client.logout()
        resp = self.client.delete(reverse(constants.COACH_URL_NAME, args=[coach.id]))
        self.assertEqual(resp.status_code, 403)
