from django.test import TestCase
from task_manager.statuses.models import Statuses
from django.test import Client
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class StatusesTest(TestCase):
    test_data = get_test_data('statuses.json')

    def test_create_status(self):
        c = Client()
        status_data = {'name': self.test_data['statuses']['status1']['name']}
        c.post('/statuses/create/', status_data)
        assert Statuses.objects.get(id=1).name == (
            self.test_data['statuses']['status1']['name'])

    def test_update_status(self):
        c = Client()
        status = test_container.create_status1()
        new_data = {'name': self.test_data['statuses']['status2']['name']}
        c.post(f'/statuses/{status.id}/update/', new_data)
        assert Statuses.objects.get(id=status.id).name == (
            self.test_data['statuses']['status2']['name'])

    def test_delete_status(self):
        c = Client()
        status = test_container.create_status1()
        c.post(f'/statuses/{status.id}/delete/')
        statuses = []
        for status in Statuses.objects.all():
            statuses.append(status)
        assert not statuses

    def test_delete_status_with_task(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        status = test_container.create_status1()
        status_id = status.id
        test_container.create_task1(status, user1, user2)
        c.force_login(user1)
        c.post(f'/statuses/{status.id}/delete/')
        assert Statuses.objects.get(id=status_id).name == (
            self.test_data['statuses']['status1']['name'])
