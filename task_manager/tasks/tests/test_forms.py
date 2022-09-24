from django.test import TestCase
from task_manager.tasks.forms import TaskCreationForm
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class TaskFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')
        cls.status = test_container.create_status('status1')
        cls.task1_data = get_test_data('tasks.json')['tasks']['task1']
        cls.name = cls.task1_data['name']
        cls.description = cls.task1_data['description']

    def test_valid_form(self):
        data = {'name': self.name,
                'description': self.description,
                'status': self.status,
                'executor': self.user}
        form = TaskCreationForm(data=data)
        self.assertTrue(form.is_valid())
        data = {'name': self.name,
                'description': self.description,
                'status': self.status,
                'executor': ''}
        form = TaskCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'name': '',
                'description': self.description,
                'status': self.status,
                'executor': self.user}
        form = TaskCreationForm(data=data)
        self.assertFalse(form.is_valid())
        data = {'name': self.name,
                'description': '',
                'status': self.status,
                'executor': self.user}
        form = TaskCreationForm(data=data)
        self.assertFalse(form.is_valid())
