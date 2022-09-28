from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.test_container import TestContainer
from task_manager.utils import get_test_data


test_container = TestContainer()


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')
        cls.user_data = get_test_data('users.json')['users']['user1']

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, get_user_model()))
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertEqual(self.user.username, self.user_data['username'])
