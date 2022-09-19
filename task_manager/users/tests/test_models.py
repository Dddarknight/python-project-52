from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class UserModelTest(TestCase):

    def test_user_creation(self):
        user = test_container.create_user1()
        self.assertTrue(isinstance(user, get_user_model()))
