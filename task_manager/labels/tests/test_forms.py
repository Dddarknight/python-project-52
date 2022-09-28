from django.test import TestCase

from task_manager.labels.forms import LabelCreationForm
from task_manager.test_container import TestContainer
from task_manager.utils import get_test_data


test_container = TestContainer()


class LabelFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.label1_data = (
            get_test_data('labels.json')['labels']['label1'])
        cls.name = cls.label1_data['name']

    def test_valid_form(self):
        data = {'name': self.name}
        form = LabelCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        test_container.create_label('label1')
        data = {'name': self.name}
        form = LabelCreationForm(data=data)
        self.assertFalse(form.is_valid())
