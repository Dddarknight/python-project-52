from django.test import TestCase

from task_manager.labels.models import Labels
from task_manager.test_container import TestContainer
from task_manager.utils import get_test_data


test_container = TestContainer()


class LabelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.label = test_container.create_label('label1')
        cls.label_data = get_test_data('labels.json')['labels']['label1']

    def test_status_creation(self):
        self.assertTrue(isinstance(self.label, Labels))
        self.assertEqual(self.label.name, self.label_data['name'])
