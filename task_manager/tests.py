from django.test import TestCase
from task_manager.users.models import HexletUser
from task_manager.statuses.models import Statuses
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
from task_manager.utils import get_test_data


class TestObjectsCreation(TestCase):
    test_data_users = get_test_data('users.json')
    test_data_statuses = get_test_data('statuses.json')
    test_data_tasks = get_test_data('tasks.json')
    test_data_labels = get_test_data('labels.json')

    def create_user1(self):
        return HexletUser.objects.create(
            first_name=self.test_data_users['users']['user1']['first_name'],
            last_name=self.test_data_users['users']['user1']['last_name'],
            username=self.test_data_users['users']['user1']['username'],
            password=self.test_data_users['users']['user1']['password'])

    def create_user2(self):
        return HexletUser.objects.create(
            first_name=self.test_data_users['users']['user2']['first_name'],
            last_name=self.test_data_users['users']['user2']['last_name'],
            username=self.test_data_users['users']['user2']['username'],
            password=self.test_data_users['users']['user2']['password'])

    def create_status1(self):
        return Statuses.objects.create(
            name=self.test_data_statuses['statuses']['status1']['name'])

    def create_status2(self):
        return Statuses.objects.create(
            name=self.test_data_statuses['statuses']['status2']['name'])

    def create_task1(self, status, author, executor):
        return Tasks.objects.create(
            name=self.test_data_tasks['tasks']['task1']['name'],
            description=self.test_data_tasks['tasks']['task1']['name'],
            status=status,
            author=author,
            executor=executor)
    
    def create_task2(self, status, author, executor):
        return Tasks.objects.create(
            name=self.test_data_tasks['tasks']['task2']['name'],
            description=self.test_data_tasks['tasks']['task2']['name'],
            status=status,
            author=author,
            executor=executor)
    
    def create_task3(self, status, author, executor):
        return Tasks.objects.create(
            name=self.test_data_tasks['tasks']['task3']['name'],
            description=self.test_data_tasks['tasks']['task3']['name'],
            status=status,
            author=author,
            executor=executor)

    def create_label1(self):
        return Labels.objects.create(
            name=self.test_data_labels['labels']['label1']['name'])

    def create_label2(self):
        return Labels.objects.create(
            name=self.test_data_labels['labels']['label2']['name'])

    def create_label3(self):
        return Labels.objects.create(
            name=self.test_data_labels['labels']['label3']['name'])
