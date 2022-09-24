from django.test import TestCase
from task_manager.labels.models import Labels
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class LabelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.label = test_container.create_label('label1')

    def test_status_creation(self):
        self.assertTrue(isinstance(self.label, Labels))
