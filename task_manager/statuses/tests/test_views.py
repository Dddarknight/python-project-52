from django.test import TestCase
from task_manager.statuses.models import Statuses
from django.test import Client
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation
from django.urls import reverse_lazy


test_container = TestObjectsCreation()


class StatusCreationTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.status1_data = (
            get_test_data('statuses.json')['statuses']['status1'])
        cls.name = cls.status1_data['name']

    def test_create_status(self):
        c = Client()
        status_data = {'name': self.name}
        c.post('/statuses/create/', status_data)
        assert Statuses.objects.get(id=1).name == (
            self.name)


class StatusUpdateDeleteTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user1 = test_container.create_user('user1')
        cls.status1 = test_container.create_status('status1')
        cls.status1_data = (
            get_test_data('statuses.json')['statuses']['status1'])
        cls.name1 = cls.status1_data['name']
        cls.status2_data = (
            get_test_data('statuses.json')['statuses']['status2'])
        cls.name2 = cls.status2_data['name']

    def test_update_status(self):
        c = Client()
        c.force_login(self.user1)
        new_data = {'name': self.name2}
        c.post(f'/statuses/{self.status1.id}/update/', data=new_data)
        assert Statuses.objects.get(id=self.status1.id).name == (
            self.name2)

    def test_delete_status(self):
        c = Client()
        c.force_login(self.user1)
        c.post(f'/statuses/{self.status1.id}/delete/')
        statuses = []
        for status in Statuses.objects.all():
            statuses.append(status)
        assert not statuses


class StatusDeleteDeniedTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.task = test_container.create_task(
            'task1', cls.status, cls.user1, cls.user2)
        cls.status1_data = (
            get_test_data('statuses.json')['statuses']['status1'])
        cls.name1 = cls.status1_data['name']

    def test_delete_status_with_task(self):
        c = Client()
        status_id = self.status.id
        c.force_login(self.user1)
        c.post(f'/statuses/{self.status.id}/delete/')
        assert Statuses.objects.get(id=status_id).name == (
            self.name1)


class StatusViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')
        cls.status = test_container.create_status('status1')

    def test_create_view(self):
        c = Client()
        response = c.get(reverse_lazy('status_create'))
        required_content_elements = ['Имя']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_create.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_update_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('status_update', args=['1']))
        required_content_elements = ['Имя']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_update.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_delete_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('status_delete', args=['1']))
        required_content_elements = [
            'Удаление статуса',
            'Вы уверены, что хотите удалить status1 ?']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_delete.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_statuses_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('statuses'))
        required_content_elements = [
            'ID', 'Имя', 'Дата создания',
            'Изменить', 'Удалить',
            '1', 'status1']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/statuses.html')
        for element in required_content_elements:
            self.assertContains(response, element)
