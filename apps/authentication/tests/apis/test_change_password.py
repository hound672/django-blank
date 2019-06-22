# -*- coding: utf-8 -*-
"""
    test_change_password
    ~~~~~~~~~~~~~~~
  

"""

from unittest.mock import patch

from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from utils.faker import faker

from apps.users.factories import BaseUserFactory


class TestChangePassword(APITestCase):
    def setUp(self):
        self._username = faker.user_name()
        self._password = faker.password()
        self._user = BaseUserFactory(username=self._username)
        self._user.set_password(self._password)
        self._user.is_active = True
        self._user.save()
        self._url_login = reverse('api:auth:login')
        self._url_logout = reverse('api:auth:logout')
        self._url_change_password = reverse('api:auth:change-password')
        self._data = {
            'username': self._username,
            'password': self._password
        }

    @patch('apps.authentication.apis.get_user_data')
    def test_logged_out_user_cannot_change_password(self, mock_object):
        mock_object.return_value = {}
        self._user.is_active = True
        self._user.save()

        # this should perform login
        res_login = self.client.post(self._url_login, data=self._data)
        token = res_login.data['token']

        # perform logout
        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        self.client.post(self._url_logout)

        data = {
            "old_password": self._password,
            "new_password": faker.password(),
        }

        # this should perform change password
        res_change_pass = self.client.post(
            self._url_change_password,
            data=data
        )

        self.assertEqual(res_change_pass.status_code, 401)

    @patch('apps.authentication.apis.get_user_data')
    def test_inactive_user_cannot_change_password(self, mock_object):
        mock_object.return_value = {}
        self._user.is_active = True
        self._user.save()

        # this should perform login
        res_login = self.client.post(self._url_login, data=self._data)

        token = res_login.data['token']

        self._user.is_active = False
        self._user.save()

        data = {
            'old_password': self._password,
            'new_password': faker.password(),
        }

        # this should perform change password
        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        change_password_response = self.client.post(
            self._url_change_password,
            data=data,
        )

        self.assertEqual(change_password_response.status_code, 401)

    @patch('apps.authentication.apis.get_user_data')
    def test_user_cannot_change_password_with_invalid_token(self, mock_object):
        mock_object.return_value = {}
        self._user.is_active = True
        self._user.save()

        # this should perform login
        res_login = self.client.post(self._url_login, data=self._data)

        token = res_login.data['token']

        self._user.rotate_secret_key()

        data = {
            'old_password': self._password,
            'new_password': faker.password(),
        }

        # this should perform change password
        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        change_password_response = self.client.post(
            self._url_change_password,
            data=data,
        )

        self.assertEqual(change_password_response.status_code, 401)

    @patch('apps.authentication.apis.get_user_data')
    def test_user_cannot_change_password_with_wrong_old_password(self, mock_object):
        mock_object.return_value = {}
        self._user.is_active = True
        self._user.save()

        # this should perform login
        res_login = self.client.post(self._url_login, data=self._data)

        token = res_login.data['token']

        data = {
            "old_password": faker.password(),
            "new_password": faker.password(),
        }

        # this should perform change password
        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        change_password_response = self.client.post(
            self._url_change_password,
            data=data,
        )

        self.assertEqual(change_password_response.status_code, 400)

    @patch('apps.authentication.apis.change_user_password')
    @patch('apps.authentication.apis.get_user_data')
    def test_active_user_can_change_password_with_valid_token(self, mock1, mock2):
        mock1.return_value = {}
        self._user.is_active = True
        self._user.save()

        # this should perform login
        login_response = self.client.post(self._url_login, data=self._data)

        token = login_response.data['token']

        data = {
            "old_password": self._password,
            "new_password": faker.password(),
        }

        # this should perform change password
        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        change_password_response = self.client.post(
            self._url_change_password,
            data=data,
        )

        self.assertTrue(mock2.called)
        self.assertEqual(change_password_response.status_code, 202)
