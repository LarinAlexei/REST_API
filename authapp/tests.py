from django.test import TestCase
from requests import request, post, get
from rest_framework.test import CoreAPIClient
from coreapi import Client


# Create your tests here.


class TestToken(TestCase):

    def setUp(self):
        self.data = {'username': 'Larin', 'password': 'geek'}
        self.password = 'geek'
        self.url_token = 'http://127.0.0.1:8000/api-token-auth/'
        self.url_jwt_token = 'http://127.0.0.1:8000/api/token/'
        self.url_prob = 'http://127.0.0.1:8000/api/project/'

    def query_no_token(self):
        response = post(self.url_prob)
        self.assertEqual(response.status_code, 401)

    def authorization_token(self):
        response = post(self.url_token, data=self.data)
        self.assertEqual(response.status_code, 200)
        token = response.json().get('token')
        response_test = get(self.url_prob, headers={'Authorization': f'Token {token}'})
        self.assertEqual(response_test.status_code, 200)

    def query_jwt_token(self):
        response = post(self.url_jwt_token, data=self.data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        access_token = response_json.get('access')
        refresh_token = response_json.get('refresh')
        response_test = get(self.url_prob, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response_test.status_code, 200)
        response_refresh = get(self.url_jwt_token, data={'refresh': refresh_token})
        access_refresh_token = response_refresh.json().get('access')
        self.assertNotEqual(access_token, access_refresh_token)
