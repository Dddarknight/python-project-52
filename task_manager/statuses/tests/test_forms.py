from django.test import TestCase

from task_manager.statuses.forms import StatusCreationForm
from task_manager.test_container import TestContainer
from task_manager.utils import get_test_data


test_container = TestContainer()


class StatusFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.status1_data = (
            get_test_data('statuses.json')['statuses']['status1'])
        cls.name = cls.status1_data['name']

    def test_valid_form(self):
        data = {'name': self.name}
        form = StatusCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        test_container.create_status('status1')
        data = {'name': self.name}
        form = StatusCreationForm(data=data)
        self.assertFalse(form.is_valid())
