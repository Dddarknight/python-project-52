from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, get_user_model()))
