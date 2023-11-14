import os
from django.test import TestCase
from django.contrib.auth.password_validation import validate_password


class MyTestCases(TestCase):
    def test_key(self):
        KEY = os.environ.get('SECRET_KEY')
        self.assertAlmostEqual
        try:
            validate_password(KEY)
        except Exception as e:
            message = e.messages
            self.fail(msg=message)
