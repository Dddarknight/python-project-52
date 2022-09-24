from django.test import TestCase
from task_manager.users.forms import UserRegistrationForm
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation


test_container = TestObjectsCreation()


class UserFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1_data = get_test_data('users.json')['users']['user1']
        cls.first_name = cls.user1_data['first_name']
        cls.last_name = cls.user1_data['last_name']
        cls.username = cls.user1_data['username']
        cls.password = cls.user1_data['password']

    def test_valid_form(self):
        data = {'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username,
                'password1': self.password,
                'password2': self.password}
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_without_requied_fields(self):
        data1 = {'first_name': self.first_name,
                 'last_name': self.last_name,
                 'username': self.username,
                 'password1': self.password}
        form = UserRegistrationForm(data=data1)
        self.assertFalse(form.is_valid())
        data2 = {'first_name': self.first_name,
                 'last_name': '',
                 'username': self.username,
                 'password1': self.password,
                 'password2': self.password}
        form = UserRegistrationForm(data=data2)
        self.assertFalse(form.is_valid())
        data3 = {'first_name': '',
                 'last_name': self.last_name,
                 'username': self.username,
                 'password1': self.password,
                 'password2': self.password}
        form = UserRegistrationForm(data=data3)
        self.assertFalse(form.is_valid())
        data4 = {'first_name': self.first_name,
                 'last_name': self.last_name,
                 'username': '',
                 'password1': self.password,
                 'password2': self.password}
        form = UserRegistrationForm(data=data4)
        self.assertFalse(form.is_valid())
