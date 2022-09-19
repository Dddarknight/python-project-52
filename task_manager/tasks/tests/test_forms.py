from django.test import TestCase
from task_manager.tasks.forms import TaskCreationForm
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class TaskFormTest(TestCase):
    test_data = get_test_data('tasks.json')

    def test_valid_form(self):
        user = test_container.create_user1()
        status = test_container.create_status1()
        data = {'name': self.test_data['tasks']['task1']['name'],
                'description': self.test_data['tasks']['task1']['description'],
                'status': status,
                'executor': user}
        form = TaskCreationForm(data=data)
        self.assertTrue(form.is_valid())
        data = {'name': self.test_data['tasks']['task1']['name'],
                'description': self.test_data['tasks']['task1']['description'],
                'status': status,
                'executor': ''}
        form = TaskCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = test_container.create_user1()
        status = test_container.create_status1()
        data = {'name': '',
                'description': self.test_data['tasks']['task1']['description'],
                'status': status,
                'executor': user}
        form = TaskCreationForm(data=data)
        self.assertFalse(form.is_valid())
        data = {'name': self.test_data['tasks']['task1']['name'],
                'description': '',
                'status': status,
                'executor': user}
        form = TaskCreationForm(data=data)
        self.assertFalse(form.is_valid())
