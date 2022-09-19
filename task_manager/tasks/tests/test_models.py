from django.test import TestCase
from task_manager.tasks.models import Tasks
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class TaskModelTest(TestCase):

    def test_status_creation(self):
        user = test_container.create_user1()
        status = test_container.create_status1()
        task = test_container.create_task1(status, user, user)
        self.assertTrue(isinstance(task, Tasks))
