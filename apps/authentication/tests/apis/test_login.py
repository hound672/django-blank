# -*- coding: utf-8 -*-
"""
    test_login
    ~~~~~~~~~~~~~~~
  

"""

from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from utils.faker import faker

from apps.users.factories import BaseUserFactory


class TestLogin(APITestCase):
    def setUp(self):
        self._username = faker.user_name()
        self._password = faker.password()
        self._user = BaseUserFactory(username=self._username)
        self._user.set_password(self._password)
        self._user.is_active = True
        self._user.save()
        self._url_login = reverse('api:auth:login')

    def test_user_login_success(self):
        data = {
            'username': self._username,
            'password': self._password
        }
        res = self.client.post(self._url_login, data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_login_wrong_username(self):
        data = {
            'username': faker.user_name,
            'password': self._password
        }
        res = self.client.post(self._url_login, data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_wrong_password(self):
        data = {
            'username': self._username,
            'password': faker.password()
        }
        res = self.client.post(self._url_login, data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_inactive(self):
        self._user.is_active = False
        self._user.save()

        data = {
            'username': self._username,
            'password': self._password
        }
        res = self.client.post(self._url_login, data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
