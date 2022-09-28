from django.contrib.auth import get_user_model
from django.test import TestCase
from task_manager.labels.models import Labels
from task_manager.statuses.models import Statuses
from task_manager.tasks.models import Tasks
from task_manager.utils import get_test_data


class TestContainer(TestCase):
    test_data_users = get_test_data('users.json')
    test_data_statuses = get_test_data('statuses.json')
    test_data_tasks = get_test_data('tasks.json')
    test_data_labels = get_test_data('labels.json')

    def create_user(self, user):
        return get_user_model().objects.create(
            first_name=self.test_data_users['users'][user]['first_name'],
            last_name=self.test_data_users['users'][user]['last_name'],
            username=self.test_data_users['users'][user]['username'],
            password=self.test_data_users['users'][user]['password'])

    def create_status(self, status):
        return Statuses.objects.create(
            name=self.test_data_statuses['statuses'][status]['name'])

    def create_task(self, task, status, author, executor):
        return Tasks.objects.create(
            name=self.test_data_tasks['tasks'][task]['name'],
            description=self.test_data_tasks['tasks'][task]['name'],
            status=status,
            author=author,
            executor=executor)

    def create_label(self, label):
        return Labels.objects.create(
            name=self.test_data_labels['labels'][label]['name'])
