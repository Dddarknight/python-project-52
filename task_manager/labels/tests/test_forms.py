from django.test import TestCase
from task_manager.labels.forms import LabelCreationForm
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class LabelFormTest(TestCase):
    test_data = get_test_data('labels.json')

    def test_valid_form(self):
        data = {'name': self.test_data['labels']['label1']['name']}
        form = LabelCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        test_container.create_label1()
        data = {'name': self.test_data['labels']['label1']['name']}
        form = LabelCreationForm(data=data)
        self.assertFalse(form.is_valid())
