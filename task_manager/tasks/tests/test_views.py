from django.test import TestCase
from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskCreationForm
from django.test import Client
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation
from django.urls import reverse_lazy


test_container = TestObjectsCreation()


class TaskCreationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.task1_data = get_test_data('tasks.json')['tasks']['task1']
        cls.name = cls.task1_data['name']
        cls.description = cls.task1_data['description']

    def test_create_task(self):
        c = Client()
        c.force_login(self.user1)
        task_data = {
            'name': self.name,
            'description': self.description,
            'status': self.status.id,
            'executor': self.user2.id}
        c.post('/tasks/create/', task_data)
        assert Tasks.objects.get(id=1).name == (
            self.name)
        assert Tasks.objects.get(id=1).description == (
            self.description)
        assert Tasks.objects.get(id=1).executor == self.user2
        assert Tasks.objects.get(id=1).status == self.status
        assert Tasks.objects.get(id=1).author == self.user1


class TaskUpdateDeleteTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.task1 = test_container.create_task(
            'task1', cls.status, cls.user1, cls.user2)
        cls.task2 = test_container.create_task(
            'task2', cls.status, cls.user2, cls.user1)
        cls.task1_data = get_test_data('tasks.json')['tasks']['task1']
        cls.task2_data = get_test_data('tasks.json')['tasks']['task2']
        cls.task3_data = get_test_data('tasks.json')['tasks']['task3']
        cls.name1 = cls.task1_data['name']
        cls.description1 = cls.task1_data['description']
        cls.name2 = cls.task2_data['name']
        cls.description2 = cls.task2_data['description']
        cls.name3 = cls.task3_data['name']
        cls.description3 = cls.task3_data['description']

    def test_update_task(self):
        c = Client()
        c.force_login(self.user1)
        new_data = {'name': self.name2,
                    'description': self.description1,
                    'status': self.status.id,
                    'executor': self.user1.id}
        c.post(f'/tasks/{self.task1.id}/update/', new_data)
        assert Tasks.objects.get(id=self.task1.id).name == (
            self.name1)
        assert Tasks.objects.get(id=self.task1.id).executor == self.user2
        new_data = {'name': self.name3,
                    'description': self.description1,
                    'status': self.status.id,
                    'executor': self.user1.id}
        c.post(f'/tasks/{self.task1.id}/update/', new_data)
        assert Tasks.objects.get(id=self.task1.id).name == (
            self.name3)
        assert Tasks.objects.get(id=self.task1.id).executor == self.user1

    def test_delete_task(self):
        c = Client()
        c.force_login(self.user1)
        c.post(f'/tasks/{self.task1.id}/delete/')
        c.force_login(self.user2)
        c.post(f'/tasks/{self.task2.id}/delete/')
        tasks = []
        for task in Tasks.objects.all():
            tasks.append(task)
        assert not tasks


class TaskFilterAndNoPermissionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status1 = test_container.create_status('status1')
        cls.status2 = test_container.create_status('status2')
        cls.label1 = test_container.create_label('label1')
        cls.label2 = test_container.create_label('label2')
        cls.label3 = test_container.create_label('label3')
        cls.task1 = test_container.create_task(
            'task1', cls.status1, cls.user1, cls.user2)
        cls.task1.labels.add(cls.label1)
        cls.task1.labels.add(cls.label2)
        cls.task2 = test_container.create_task(
            'task2', cls.status2, cls.user2, cls.user1)
        cls.task2.labels.add(cls.label3)
        cls.task3 = test_container.create_task(
            'task3', cls.status2, cls.user1, cls.user2)
        cls.task3.labels.add(cls.label1)
        cls.task1_data = get_test_data('tasks.json')['tasks']['task1']
        cls.name1 = cls.task1_data['name']

    def test_filter(self):
        c = Client()
        c.force_login(self.user1)
        data1 = {'status': self.status1.id,
                 'executor': '',
                 'labels': '',
                 'only_author': ''}
        response = c.get('/tasks/', data1)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
        data2 = {'status': self.status2.id,
                 'executor': self.user1.id,
                 'labels': '',
                 'only_author': ''}
        response = c.get('/tasks/', data2)
        self.assertNotContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
        data3 = {'status': '',
                 'executor': '',
                 'labels': '',
                 'only_author': True}
        response = c.get('/tasks/', data3)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)
        data4 = {'status': self.status1.id,
                 'executor': '',
                 'labels': '',
                 'only_author': True}
        response = c.get('/tasks/', data4)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
        data5 = {'status': '',
                 'executor': '',
                 'labels': self.label1.id,
                 'only_author': ''}
        response = c.get('/tasks/', data5)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)
        data6 = {'status': self.status2.id,
                 'executor': '',
                 'labels': self.label1.id,
                 'only_author': ''}
        response = c.get('/tasks/', data6)
        self.assertNotContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_delete_task_by_not_author(self):
        c = Client()
        c.force_login(self.user2)
        c.post(f'/tasks/{self.task1.id}/delete/')
        assert Tasks.objects.get(id=self.task1.id).name == (
            self.name1)
        assert Tasks.objects.get(id=self.task1.id).author == self.user1
        assert Tasks.objects.get(id=self.task1.id).executor == self.user2


class TaskViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')
        cls.status = test_container.create_status('status1')
        cls.task1 = test_container.create_task(
            'task1', cls.status, cls.user, cls.user)

    def test_create_view(self):
        c = Client()
        response = c.get(reverse_lazy('task_create'))
        required_content_elements = ['Имя', 'Описание', 'Статус',
                                     'Исполнитель', 'Метки']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_create.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_update_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('task_update', args=['1']))
        required_content_elements = ['Имя', 'Описание', 'Статус',
                                     'Исполнитель', 'Метки']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_update.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_delete_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('task_delete', args=['1']))
        required_content_elements = [
            'Удаление задачи',
            'Вы уверены, что хотите удалить task1 ?']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_delete.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_tasks_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('tasks'))
        required_content_elements = [
            'ID', 'Имя', 'Статус', 'Автор', 'Исполнитель', 'Дата создания',
            'Изменить', 'Удалить',
            '1', 'task1', 'status1', 'John Black', 'John Black']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_filter.html')
        for element in required_content_elements:
            self.assertContains(response, element)
