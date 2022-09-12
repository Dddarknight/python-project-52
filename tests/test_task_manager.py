from django.test import TestCase
from task_manager.models import HexletUser, Statuses, Tasks, Labels
from task_manager.forms import UserRegistrationForm
from django.test import Client


class UserTest(TestCase):

    def create_user(self):
        return HexletUser.objects.create(first_name="John",
                                         last_name="Black",
                                         username="johnblack",
                                         password='*aaaccc3')

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, HexletUser))

    def test_valid_form(self):
        data = {'first_name': "John",
                'last_name': "Black",
                'username': "johnblack",
                'password1': '*aaaccc3',
                'password2': '*aaaccc3'}
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form1(self):
        data = {'first_name': "John",
                'last_name': "Black",
                'username': "johnblack",
                'password': '*aaaccc3'}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form2(self):
        data = {'first_name': "John",
                'last_name': "",
                'username': "johnblack",
                'password1': '*aaaccc3',
                'password2': '*aaaccc3'}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_register_user(self):
        c = Client()
        user_data = {'first_name': "Jack",
                     'last_name': "Black",
                     'username': "johnbl",
                     'password1': '*aaaccc6',
                     'password2': '*aaaccc6'}
        c.post('/users/create/', user_data)
        assert HexletUser.objects.get(id=1).first_name == "Jack"
        assert HexletUser.objects.get(id=1).username == "johnbl"

    def test_update_user(self):
        c = Client()
        user = HexletUser.objects.create(first_name="John",
                                         last_name="Black",
                                         username="johnblack",
                                         password='*aaaccc3')
        new_data = {'first_name': "Jack",
                    'last_name': "Black",
                    'username': "johnbl",
                    'password1': '*aaaccc6',
                    'password2': '*aaaccc6'}
        c.post(f'/users/{user.id}/update/', new_data)
        assert HexletUser.objects.get(id=user.id).first_name == "Jack"
        assert HexletUser.objects.get(id=user.id).username == "johnbl"

    def test_delete_user(self):
        c = Client()
        user = HexletUser.objects.create(first_name="John",
                                         last_name="Black",
                                         username="johnblack",
                                         password='*aaaccc3')
        c.post(f'/users/{user.id}/delete/')
        users = []
        for user in HexletUser.objects.all():
            users.append(user)
        assert not users

    def test_create_status(self):
        c = Client()
        status_data = {'name': "status1"}
        c.post('/statuses/create/', status_data)
        assert Statuses.objects.get(id=1).name == "status1"

    def test_update_status(self):
        c = Client()
        status = Statuses.objects.create(name="status1")
        new_data = {'name': "status2"}
        c.post(f'/statuses/{status.id}/update/', new_data)
        assert Statuses.objects.get(id=status.id).name == "status2"

    def test_delete_status(self):
        c = Client()
        status = Statuses.objects.create(name="status1")
        c.post(f'/statuses/{status.id}/delete/')
        statuses = []
        for status in Statuses.objects.all():
            statuses.append(status)
        assert not statuses

    def test_create_task(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        user2 = HexletUser.objects.create(first_name="Bob",
                                          last_name="Green",
                                          username="bobgreen",
                                          password='*aaaccc5')
        c.force_login(user1)
        status = Statuses.objects.create(name="status1")
        task_data = {'name': "task1",
                     'description': 'some_description',
                     'status': status.id,
                     'executor': user2.id}
        c.post('/tasks/create/', task_data)
        assert Tasks.objects.get(id=1).name == "task1"
        assert Tasks.objects.get(id=1).description == "some_description"
        assert Tasks.objects.get(id=1).executor == user2
        assert Tasks.objects.get(id=1).status.name == "status1"
        assert Tasks.objects.get(id=1).author == user1

    def test_update_task(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        user2 = HexletUser.objects.create(first_name="Bob",
                                          last_name="Green",
                                          username="bobgreen",
                                          password='*aaaccc5')
        status = Statuses.objects.create(name="status1")
        task1 = Tasks.objects.create(name="task1",
                                     description='some_description1',
                                     status=status,
                                     author=user1,
                                     executor=user2)
        Tasks.objects.create(name="task2",
                             description='some_description2',
                             status=status,
                             author=user2,
                             executor=user1)
        new_data = {'name': "task2",
                    'description': 'some_description',
                    'status': status.id,
                    'executor': user1.id}
        c.post(f'/tasks/{task1.id}/update/', new_data)
        assert Tasks.objects.get(id=task1.id).name == "task1"
        assert Tasks.objects.get(id=task1.id).executor == user2
        new_data = {'name': "task3",
                    'description': 'some_description3',
                    'status': status.id,
                    'executor': user1.id}
        c.post(f'/tasks/{task1.id}/update/', new_data)
        assert Tasks.objects.get(id=task1.id).name == "task3"
        assert Tasks.objects.get(id=task1.id).executor == user1

    def test_delete_task(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        user2 = HexletUser.objects.create(first_name="Bob",
                                          last_name="Green",
                                          username="bobgreen",
                                          password='*aaaccc5')
        status = Statuses.objects.create(name="status1")
        task = Tasks.objects.create(name="task",
                                    description='some_description',
                                    status=status,
                                    author=user1,
                                    executor=user2)
        c.force_login(user1)
        c.post(f'/tasks/{task.id}/delete/')
        tasks = []
        for task in Tasks.objects.all():
            tasks.append(task)
        assert not tasks

    def test_delete_task_by_not_author(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        user2 = HexletUser.objects.create(first_name="Bob",
                                          last_name="Green",
                                          username="bobgreen",
                                          password='*aaaccc5')
        status = Statuses.objects.create(name="status1")
        task = Tasks.objects.create(name="task",
                                    description='some_description',
                                    status=status,
                                    author=user1,
                                    executor=user2)
        c.force_login(user2)
        c.post(f'/tasks/{task.id}/delete/')
        assert Tasks.objects.get(id=task.id).name == "task"
        assert Tasks.objects.get(id=task.id).author == user1
        assert Tasks.objects.get(id=task.id).executor == user2

    def test_delete_user_status_with_task(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        user2 = HexletUser.objects.create(first_name="Bob",
                                          last_name="Green",
                                          username="bobgreen",
                                          password='*aaaccc5')
        user1_id = user1.id
        user2_id = user2.id
        status = Statuses.objects.create(name="status1")
        status_id = status.id
        Tasks.objects.create(name="task",
                             description='some_description',
                             status=status,
                             author=user1,
                             executor=user2)
        c.force_login(user1)
        c.post(f'/users/{user1.id}/delete/')
        assert HexletUser.objects.get(id=user1_id).username == "johnblack"
        c.force_login(user2)
        c.post(f'/users/{user2.id}/delete/')
        assert HexletUser.objects.get(id=user2_id).username == "bobgreen"
        c.post(f'/statuses/{status.id}/delete/')
        assert Statuses.objects.get(id=status_id).name == "status1"

    def test_create_label(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        c.force_login(user1)
        label_data = {'name': "label1"}
        c.post('/labels/create/', label_data)
        assert Labels.objects.get(id=1).name == "label1"

    def test_update_label(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        c.force_login(user1)
        label1 = Labels.objects.create(name="label1")
        Labels.objects.create(name="label2")
        new_data_invalid = {'name': "label2"}
        c.post(f'/labels/{label1.id}/update/', new_data_invalid)
        assert Labels.objects.get(id=label1.id).name == "label1"
        new_data_valid = {'name': "label3"}
        c.post(f'/labels/{label1.id}/update/', new_data_valid)
        assert Labels.objects.get(id=label1.id).name == "label3"

    def test_delete_label(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        label1 = Labels.objects.create(name="label1")
        c.force_login(user1)
        c.post(f'/labels/{label1.id}/delete/')
        labels = []
        for label in Labels.objects.all():
            labels.append(label)
        assert not labels

    def test_delete_label_with_task(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        user2 = HexletUser.objects.create(first_name="Bob",
                                          last_name="Green",
                                          username="bobgreen",
                                          password='*aaaccc5')
        status = Statuses.objects.create(name="status1")
        label1 = Labels.objects.create(name="label1")
        label1_id = label1.id
        label2 = Labels.objects.create(name="label2")
        task = Tasks.objects.create(name="task",
                                    description='some_description',
                                    status=status,
                                    author=user1,
                                    executor=user2)
        task.labels.add(label1)
        task.labels.add(label2)
        c.force_login(user1)
        c.post(f'/labels/{label1.id}/delete/')
        assert Labels.objects.get(id=label1_id).name == "label1"

    def test_filter(self):
        c = Client()
        user1 = HexletUser.objects.create(first_name="John",
                                          last_name="Black",
                                          username="johnblack",
                                          password='*aaaccc3')
        user2 = HexletUser.objects.create(first_name="Bob",
                                          last_name="Green",
                                          username="bobgreen",
                                          password='*aaaccc5')
        status1 = Statuses.objects.create(name="status1")
        status2 = Statuses.objects.create(name="status2")
        label1 = Labels.objects.create(name="label1")
        label2 = Labels.objects.create(name="label2")
        label3 = Labels.objects.create(name="label3")
        task1 = Tasks.objects.create(name="task1",
                                     description='some_description',
                                     status=status1,
                                     author=user1,
                                     executor=user2)
        task1.labels.add(label1)
        task1.labels.add(label2)
        task2 = Tasks.objects.create(name="task2",
                                     description='some_description',
                                     status=status2,
                                     author=user2,
                                     executor=user1)
        task2.labels.add(label3)
        task3 = Tasks.objects.create(name="task3",
                                     description='some_description',
                                     status=status2,
                                     author=user1,
                                     executor=user2)
        task3.labels.add(label1)
        c.force_login(user1)
        data1 = {'status': status1.id,
                 'executor': '',
                 'labels': '',
                 'only_author': ''}
        response = c.get('/tasks/', data1)
        self.assertContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertNotContains(response, 'task3')
        data2 = {'status': status2.id,
                 'executor': user1.id,
                 'labels': '',
                 'only_author': ''}
        response = c.get('/tasks/', data2)
        self.assertNotContains(response, 'task1')
        self.assertContains(response, 'task2')
        self.assertNotContains(response, 'task3')
        data3 = {'status': '',
                 'executor': '',
                 'labels': '',
                 'only_author': True}
        response = c.get('/tasks/', data3)
        self.assertContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertContains(response, 'task3')
        data4 = {'status': status1.id,
                 'executor': '',
                 'labels': '',
                 'only_author': True}
        response = c.get('/tasks/', data4)
        self.assertContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertNotContains(response, 'task3')
        data5 = {'status': '',
                 'executor': '',
                 'labels': label1.id,
                 'only_author': ''}
        response = c.get('/tasks/', data5)
        self.assertContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertContains(response, 'task3')
        data6 = {'status': status2.id,
                 'executor': '',
                 'labels': label1.id,
                 'only_author': ''}
        response = c.get('/tasks/', data6)
        self.assertNotContains(response, 'task1')
        self.assertNotContains(response, 'task2')
        self.assertContains(response, 'task3')
