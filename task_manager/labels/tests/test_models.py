from django.test import TestCase
from task_manager.labels.models import Labels
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class LabelModelTest(TestCase):

    def test_status_creation(self):
        status = test_container.create_label1()
        self.assertTrue(isinstance(status, Labels))
