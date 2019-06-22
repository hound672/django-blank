# -*- coding: utf-8 -*-
"""
    test_jwt_authorization
    ~~~~~~~~~~~~~~~
  

"""

import jwt
from jwt.exceptions import InvalidSignatureError
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from utils.faker import faker

from apps.users.factories import BaseUserFactory

class TestJwtAuthorization(APITestCase):
    def setUp(self):
        self._username = faker.user_name()
        self._password = faker.password()
        self._user = BaseUserFactory(username=self._username)
        self._user.set_password(self._password)
        self._user.is_active = True
        self._user.save()
        self._init_secret_key = self._user.secret_key
        self._url_login = reverse('api:auth:login')
        self._url_logout = reverse('api:auth:logout')
        self._url_user_detail_url = reverse('api:auth:user-detail')
        self._data = {
            'username': self._username,
            'password': self._password
        }

    def test_user_can_decode_only_own_tokens(self):
        response1 = self.client.post(self._url_login, data=self._data)

        user = BaseUserFactory()
        user.is_active = True
        password = faker.password()
        user.set_password(password)
        user.save()

        data = {
            'username': user.username,
            'password': password,
        }

        response2 = self.client.post(self._url_login, data=data)

        token_user1 = response1.data['token']
        token_user2 = response2.data['token']

        self.assertNotEqual(token_user1, token_user2)
        self.assertNotEqual(self._user.secret_key, user.secret_key)

        with self.assertRaises(InvalidSignatureError):
            jwt.decode(token_user1, key=str(user.secret_key))

        with self.assertRaises(InvalidSignatureError):
            jwt.decode(token_user2, key=str(self._user.secret_key))

        self.assertEqual(
            self._user.username,
            jwt.decode(token_user1, key=str(self._user.secret_key))['username']
        )

        self.assertEqual(
            user.username,
            jwt.decode(token_user2, key=str(user.secret_key))['username']
        )

    def test_user_access_denied_without_login(self):
        res = self.client.get(self._url_user_detail_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_access_urls_with_token_only_after_login(self):
        res = self.client.post(self._url_login, data=self._data)

        token = res.data['token']

        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        res = self.client.get(self._url_user_detail_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], self._user.username)

    def test_user_cannot_use_old_token_after_logout(self):
        res = self.client.post(self._url_login, data=self._data)
        token = res.data['token']

        # performs logout with jwt
        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        self.client.post(self._url_logout)

        response = self.client.get(self._url_user_detail_url)

        self.assertEqual(response.status_code, 401)

    def test_user_gets_new_user_secret_key_after_logout(self):
        res = self.client.post(self._url_login, data=self._data)
        token = res.data['token']

        # performs logout with jwt
        self.client.credentials(
            HTTP_AUTHORIZATION='{0:s} {1:s}'.format(api_settings.JWT_AUTH_HEADER_PREFIX, token)
        )
        self.client.post(self._url_logout)

        self._user.refresh_from_db()

        self.assertNotEqual(self._init_secret_key, self._user.secret_key)
