from django.test import TestCase

from task_manager.statuses.models import Statuses
from task_manager.test_container import TestContainer
from task_manager.utils import get_test_data


test_container = TestContainer()


class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.status = test_container.create_status('status1')
        cls.status_data = get_test_data('statuses.json')['statuses']['status1']

    def test_status_creation(self):
        self.assertTrue(isinstance(self.status, Statuses))
        self.assertEqual(self.status.name, self.status_data['name'])
