from django.test import TestCase
from task_manager.tasks.models import Tasks
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')
        cls.status = test_container.create_status('status1')
        cls.task = test_container.create_task(
            'task1', cls.status, cls.user, cls.user)

    def test_task_creation(self):
        self.assertTrue(isinstance(self.task, Tasks))
