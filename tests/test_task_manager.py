from django.test import TestCase
from task_manager.models import HexletUser, Statuses, Tasks
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
        task2 = Tasks.objects.create(name="task2",
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
        task = Tasks.objects.create(name="task",
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
