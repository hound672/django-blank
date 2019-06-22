# -*- coding: utf-8 -*-
"""
    test_models
    ~~~~~~~~~~~~~~~
  

"""

from django.test import TestCase
from django.core.exceptions import ValidationError

from utils.faker import faker
from apps.users.models import BaseUser

class TestBaseUser(TestCase):

    def setUp(self):
        self._username = faker.user_name()
        self._password = faker.password()

    def test_create_user_success_create_user(self):
        user_count = BaseUser.objects.count()
        BaseUser.objects.create_user(username=self._username,
                                     password=self._password)
        self.assertEqual(user_count + 1, BaseUser.objects.count())
    def test_create_user_raises_empty_username(self):
        with self.assertRaises(ValueError):
            BaseUser.objects.create_user(username=None,
                                         password=self._password)

    def test_user_str(self):
        user = BaseUser.objects.create_user(username=self._username,
                                     password=self._password)
        user_str = 'User: {0}'.format(self._username)
        self.assertEqual(user_str, str(user))


    def test_create_user_raises_user_exists(self):
        BaseUser.objects.create_user(username=self._username, password=self._password)
        with self.assertRaises(ValidationError):
            BaseUser.objects.create_user(username=self._username, password=self._password)