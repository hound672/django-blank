# -*- coding: utf-8 -*-
"""
    test_logout
    ~~~~~~~~~~~~~~~
  

"""

from django.test import TestCase

from django.core.exceptions import ValidationError

from apps.users.factories import BaseUserFactory
from apps.authentication.services import change_user_password

from utils.faker import faker


class TestChangeUserPassword(TestCase):
    def setUp(self):
        self._password = faker.password()
        self._user = BaseUserFactory()
        self._user.set_password(self._password)
        self._user.is_active = True
        self._user.save()
        self._init_secret_key = self._user.secret_key

    def test_user_cannot_change_password_with_wrong_old_password(self):

        with self.assertRaises(ValidationError):
            change_user_password(
                user=self._user,
                old_password=faker.password(),
                new_password=faker.password()
            )

    def test_user_cannot_change_password_with_empty_old_password(self):
        with self.assertRaises(ValidationError):
            change_user_password(
                user=self._user,
                old_password='',
                new_password=faker.password()
            )

    def test_user_cannot_change_password_with_empty_new_password(self):
        with self.assertRaises(ValidationError):
            change_user_password(
                user=self._user,
                old_password=self._password,
                new_password=''
            )

    def test_user_cannot_change_password_if_account_is_inactive(self):
        self._user.is_active = False
        self._user.save()

        with self.assertRaises(ValidationError):
            change_user_password(
                user=self._user,
                old_password=self._password,
                new_password=faker.password()
            )

    def test_user_can_change_password_with_valid_old_and_new_password_when_active(self):

        new_password = faker.password()

        change_user_password(
            user=self._user,
            old_password=self._password,
            new_password=new_password,
        )

        self._user.refresh_from_db()

        self.assertNotEqual(self._init_secret_key, self._user.secret_key)
        self.assertTrue(self._user.check_password(new_password))
