from django.test import TestCase
from task_manager.labels.models import Labels
from django.test import Client
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class UserTest(TestCase):
    test_data = get_test_data('labels.json')

    def test_create_label(self):
        c = Client()
        user1 = test_container.create_user1()
        c.force_login(user1)
        label_data = {'name': self.test_data['labels']['label1']['name']}
        c.post('/labels/create/', label_data)
        assert Labels.objects.get(id=1).name == (
            self.test_data['labels']['label1']['name'])

    def test_update_label(self):
        c = Client()
        user1 = test_container.create_user1()
        c.force_login(user1)
        label1 = test_container.create_label1()
        test_container.create_label2()
        new_data_invalid = {'name': self.test_data['labels']['label2']['name']}
        c.post(f'/labels/{label1.id}/update/', new_data_invalid)
        assert Labels.objects.get(id=label1.id).name == (
            self.test_data['labels']['label1']['name'])
        new_data_valid = {'name': self.test_data['labels']['label3']['name']}
        c.post(f'/labels/{label1.id}/update/', new_data_valid)
        assert Labels.objects.get(id=label1.id).name == (
            self.test_data['labels']['label3']['name'])

    def test_delete_label(self):
        c = Client()
        user1 = test_container.create_user1()
        label1 = test_container.create_label1()
        c.force_login(user1)
        c.post(f'/labels/{label1.id}/delete/')
        labels = []
        for label in Labels.objects.all():
            labels.append(label)
        assert not labels

    def test_delete_label_with_task(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        status = test_container.create_status1()
        label1 = test_container.create_label1()
        label1_id = label1.id
        label2 = test_container.create_label2()
        task = test_container.create_task1(status, user1, user2)
        task.labels.add(label1)
        task.labels.add(label2)
        c.force_login(user1)
        c.post(f'/labels/{label1.id}/delete/')
        assert Labels.objects.get(id=label1_id).name == "label1"
