from django.test import TestCase
from task_manager.statuses.forms import StatusCreationForm
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class StatusFormTest(TestCase):
    test_data = get_test_data('statuses.json')

    def test_valid_form(self):
        data = {'name': self.test_data['statuses']['status1']['name']}
        form = StatusCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        test_container.create_status1()
        data = {'name': self.test_data['statuses']['status1']['name']}
        form = StatusCreationForm(data=data)
        self.assertFalse(form.is_valid())
