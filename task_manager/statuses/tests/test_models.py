from django.test import TestCase
from task_manager.statuses.models import Statuses
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.status = test_container.create_status('status1')

    def test_status_creation(self):
        self.assertTrue(isinstance(self.status, Statuses))
