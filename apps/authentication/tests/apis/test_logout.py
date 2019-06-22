# -*- coding: utf-8 -*-
"""
    test_logout
    ~~~~~~~~~~~~~~~
  

"""

from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from utils.faker import faker

from apps.users.factories import BaseUserFactory

class TestLogout(APITestCase):


    def setUp(self):
        self._username = faker.user_name()
        self._password = faker.password()
        self._user = BaseUserFactory(username=self._username)
        self._user.set_password(self._password)
        self._user.is_active = True
        self._user.save()
        self._url_login = reverse('api:auth:login')
        self._url_logout = reverse('api:auth:logout')
        self._data = {
            'username': self._username,
            'password': self._password
        }

    def test_logout_with_valid_token(self):
        res_login = self.client.post(self._url_login, data=self._data)
        token = res_login.data['token']

        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        res_logout = self.client.post(self._url_logout)
        self.assertEqual(res_logout.status_code, status.HTTP_202_ACCEPTED)

    def test_logout_with_invalid_token(self):
        res_login = self.client.post(self._url_login, data=self._data)
        token = res_login.data['token']

        self._user.rotate_secret_key()

        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        res_logout = self.client.post(self._url_logout)
        self.assertEqual(res_logout.status_code, status.HTTP_401_UNAUTHORIZED)
