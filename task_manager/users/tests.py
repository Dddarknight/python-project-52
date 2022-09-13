from django.test import TestCase
from task_manager.users.models import HexletUser
from task_manager.users.forms import UserRegistrationForm
from django.test import Client
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class UserTest(TestCase):
    test_data = get_test_data('users.json')

    def test_user_creation(self):
        user = test_container.create_user1()
        self.assertTrue(isinstance(user, HexletUser))

    def test_valid_form(self):
        data = {'first_name': self.test_data['users']['user1']['first_name'],
                'last_name': self.test_data['users']['user1']['last_name'],
                'username': self.test_data['users']['user1']['username'],
                'password1': self.test_data['users']['user1']['password'],
                'password2': self.test_data['users']['user1']['password']}
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_without_requied_fields(self):
        data1 = {'first_name': self.test_data['users']['user1']['first_name'],
                 'last_name': self.test_data['users']['user1']['last_name'],
                 'username': self.test_data['users']['user1']['username'],
                 'password1': self.test_data['users']['user1']['password']}
        form = UserRegistrationForm(data=data1)
        self.assertFalse(form.is_valid())
        data2 = {'first_name': self.test_data['users']['user1']['first_name'],
                 'last_name': '',
                 'username': self.test_data['users']['user1']['username'],
                 'password1': self.test_data['users']['user1']['password'],
                 'password2': self.test_data['users']['user1']['password']}
        form = UserRegistrationForm(data=data2)
        self.assertFalse(form.is_valid())
        data3 = {'first_name': '',
                 'last_name': self.test_data['users']['user1']['last_name'],
                 'username': self.test_data['users']['user1']['username'],
                 'password1': self.test_data['users']['user1']['password'],
                 'password2': self.test_data['users']['user1']['password']}
        form = UserRegistrationForm(data=data3)
        self.assertFalse(form.is_valid())
        data4 = {'first_name': self.test_data['users']['user1']['first_name'],
                 'last_name': self.test_data['users']['user1']['last_name'],
                 'username': '',
                 'password1': self.test_data['users']['user1']['password'],
                 'password2': self.test_data['users']['user1']['password']}
        form = UserRegistrationForm(data=data4)
        self.assertFalse(form.is_valid())

    def test_register_user(self):
        c = Client()
        data = {'first_name': self.test_data['users']['user1']['first_name'],
                'last_name': self.test_data['users']['user1']['last_name'],
                'username': self.test_data['users']['user1']['username'],
                'password1': self.test_data['users']['user1']['password'],
                'password2': self.test_data['users']['user1']['password']}
        c.post('/users/create/', data)
        assert HexletUser.objects.get(id=1).first_name == (
            self.test_data['users']['user1']['first_name'])
        assert HexletUser.objects.get(id=1).last_name == (
            self.test_data['users']['user1']['last_name'])
        assert HexletUser.objects.get(id=1).username == (
            self.test_data['users']['user1']['username'])

    def test_update_user(self):
        c = Client()
        user = test_container.create_user1()
        new_data = {'first_name': (
                        self.test_data['users']['user1']['first_name']),
                    'last_name': self.test_data['users']['user1']['last_name'],
                    'username': self.test_data['users']['user2']['username'],
                    'password1': self.test_data['users']['user1']['password'],
                    'password2': self.test_data['users']['user1']['password']}
        c.post(f'/users/{user.id}/update/', new_data)
        assert HexletUser.objects.get(id=1).first_name == (
            self.test_data['users']['user1']['first_name'])
        assert HexletUser.objects.get(id=1).last_name == (
            self.test_data['users']['user1']['last_name'])
        assert HexletUser.objects.get(id=1).username == (
            self.test_data['users']['user2']['username'])

    def test_delete_user(self):
        c = Client()
        user = test_container.create_user1()
        c.post(f'/users/{user.id}/delete/')
        users = []
        for user in HexletUser.objects.all():
            users.append(user)
        assert not users

    def test_delete_user_with_task(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        user1_id = user1.id
        user2_id = user2.id
        status = test_container.create_status1()
        test_container.create_task1(status, user1, user2)
        c.force_login(user1)
        c.post(f'/users/{user1.id}/delete/')
        assert HexletUser.objects.get(id=user1_id).username == (
            self.test_data['users']['user1']['username'])
        c.force_login(user2)
        c.post(f'/users/{user2.id}/delete/')
        assert HexletUser.objects.get(id=user2_id).username == (
            self.test_data['users']['user2']['username'])
