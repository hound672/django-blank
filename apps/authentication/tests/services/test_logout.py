# -*- coding: utf-8 -*-
"""
    test_change_password
    ~~~~~~~~~~~~~~~
  

"""

from django.test import TestCase

from apps.users.factories import BaseUserFactory
from apps.authentication.services import logout


class LogoutTests(TestCase):
    def setUp(self):
        self.user = BaseUserFactory()

    def test_logout_rotates_user_secret_key(self):
        key_before = self.user.secret_key

        logout(user=self.user)
        self.user.refresh_from_db()

        self.assertNotEqual(key_before, self.user.secret_key)
