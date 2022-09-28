from django.test import TestCase

from task_manager.tasks.models import Tasks
from task_manager.test_container import TestContainer
from task_manager.utils import get_test_data


test_container = TestContainer()


class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')
        cls.status = test_container.create_status('status1')
        cls.task = test_container.create_task(
            'task1', cls.status, cls.user, cls.user)
        cls.task_data = get_test_data('tasks.json')['tasks']['task1']

    def test_task_creation(self):
        self.assertTrue(isinstance(self.task, Tasks))
        self.assertEqual(self.task.name, self.task_data['name'])
        self.assertEqual(self.task.status, self.status)
        self.assertEqual(self.task.author, self.user)
        self.assertEqual(self.task.executor, self.user)
