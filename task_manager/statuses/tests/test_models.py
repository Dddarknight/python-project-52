from django.test import TestCase
from task_manager.statuses.models import Statuses
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class StatusModelTest(TestCase):

    def test_status_creation(self):
        status = test_container.create_status1()
        self.assertTrue(isinstance(status, Statuses))
