from django.test import TestCase
from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskCreationForm
from django.test import Client
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class TasksTest(TestCase):
    test_data = get_test_data('tasks.json')

    def test_valid_form(self):
        user = test_container.create_user1()
        status = test_container.create_status1()
        data = {'name': self.test_data['tasks']['task1']['name'],
                'description': self.test_data['tasks']['task1']['description'],
                'status': status,
                'executor': user}
        form = TaskCreationForm(data=data)
        self.assertTrue(form.is_valid())
        data = {'name': self.test_data['tasks']['task1']['name'],
                'description': self.test_data['tasks']['task1']['description'],
                'status': status,
                'executor': ''}
        form = TaskCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = test_container.create_user1()
        status = test_container.create_status1()
        data = {'name': '',
                'description': self.test_data['tasks']['task1']['description'],
                'status': status,
                'executor': user}
        form = TaskCreationForm(data=data)
        self.assertFalse(form.is_valid())
        data = {'name': self.test_data['tasks']['task1']['name'],
                'description': '',
                'status': status,
                'executor': user}
        form = TaskCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_task(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        c.force_login(user1)
        status = test_container.create_status1()
        task_data = {
            'name': self.test_data['tasks']['task1']['name'],
            'description': (self.test_data['tasks']['task1']['description']),
            'status': status.id,
            'executor': user2.id}
        c.post('/tasks/create/', task_data)
        assert Tasks.objects.get(id=1).name == (
            self.test_data['tasks']['task1']['name'])
        assert Tasks.objects.get(id=1).description == (
            self.test_data['tasks']['task1']['description'])
        assert Tasks.objects.get(id=1).executor == user2
        assert Tasks.objects.get(id=1).status == status
        assert Tasks.objects.get(id=1).author == user1

    def test_update_task(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        status = test_container.create_status1()
        task1 = test_container.create_task1(status, user1, user2)
        test_container.create_task2(status, user2, user1)
        new_data = {'name': self.test_data['tasks']['task2']['name'],
                    'description': (
                        self.test_data['tasks']['task1']['description']),
                    'status': status.id,
                    'executor': user1.id}
        c.post(f'/tasks/{task1.id}/update/', new_data)
        assert Tasks.objects.get(id=task1.id).name == (
            self.test_data['tasks']['task1']['name'])
        assert Tasks.objects.get(id=task1.id).executor == user2
        new_data = {'name': self.test_data['tasks']['task3']['name'],
                    'description': (
                        self.test_data['tasks']['task1']['description']),
                    'status': status.id,
                    'executor': user1.id}
        c.post(f'/tasks/{task1.id}/update/', new_data)
        assert Tasks.objects.get(id=task1.id).name == (
            self.test_data['tasks']['task3']['name'])
        assert Tasks.objects.get(id=task1.id).executor == user1

    def test_delete_task(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        status = test_container.create_status1()
        task = test_container.create_task1(status, user1, user2)
        c.force_login(user1)
        c.post(f'/tasks/{task.id}/delete/')
        tasks = []
        for task in Tasks.objects.all():
            tasks.append(task)
        assert not tasks

    def test_filter(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        status1 = test_container.create_status1()
        status2 = test_container.create_status2()
        label1 = test_container.create_label1()
        label2 = test_container.create_label2()
        label3 = test_container.create_label3()
        task1 = test_container.create_task1(status1, user1, user2)
        task1.labels.add(label1)
        task1.labels.add(label2)
        task2 = test_container.create_task2(status2, user2, user1)
        task2.labels.add(label3)
        task3 = test_container.create_task3(status2, user1, user2)
        task3.labels.add(label1)
        c.force_login(user1)
        data1 = {'status': status1.id,
                 'executor': '',
                 'labels': '',
                 'only_author': ''}
        response = c.get('/tasks/', data1)
        self.assertContains(response, task1.name)
        self.assertNotContains(response, task2.name)
        self.assertNotContains(response, task3.name)
        data2 = {'status': status2.id,
                 'executor': user1.id,
                 'labels': '',
                 'only_author': ''}
        response = c.get('/tasks/', data2)
        self.assertNotContains(response, task1.name)
        self.assertContains(response, task2.name)
        self.assertNotContains(response, task3.name)
        data3 = {'status': '',
                 'executor': '',
                 'labels': '',
                 'only_author': True}
        response = c.get('/tasks/', data3)
        self.assertContains(response, task1.name)
        self.assertNotContains(response, task2.name)
        self.assertContains(response, task3.name)
        data4 = {'status': status1.id,
                 'executor': '',
                 'labels': '',
                 'only_author': True}
        response = c.get('/tasks/', data4)
        self.assertContains(response, task1.name)
        self.assertNotContains(response, task2.name)
        self.assertNotContains(response, task3.name)
        data5 = {'status': '',
                 'executor': '',
                 'labels': label1.id,
                 'only_author': ''}
        response = c.get('/tasks/', data5)
        self.assertContains(response, task1.name)
        self.assertNotContains(response, task2.name)
        self.assertContains(response, task3.name)
        data6 = {'status': status2.id,
                 'executor': '',
                 'labels': label1.id,
                 'only_author': ''}
        response = c.get('/tasks/', data6)
        self.assertNotContains(response, task1.name)
        self.assertNotContains(response, task2.name)
        self.assertContains(response, task3.name)

    def test_delete_task_by_not_author(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        status = test_container.create_status1()
        task = test_container.create_task1(status, user1, user2)
        c.force_login(user2)
        c.post(f'/tasks/{task.id}/delete/')
        assert Tasks.objects.get(id=task.id).name == (
            self.test_data['tasks']['task1']['name'])
        assert Tasks.objects.get(id=task.id).author == user1
        assert Tasks.objects.get(id=task.id).executor == user2
