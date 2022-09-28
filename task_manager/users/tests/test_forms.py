from django.test import TestCase
from parameterized import parameterized

from task_manager.users.forms import UserRegistrationForm
from task_manager.test_container import TestContainer
from task_manager.utils import get_test_data


test_container = TestContainer()


class UserValidFormTest(TestCase):

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


class UserInvalidFormTest(TestCase):

    user1_data = get_test_data('users.json')['users']['user1']
    first_name = user1_data['first_name']
    last_name = user1_data['last_name']
    username = user1_data['username']
    password = user1_data['password']
    testdata = [
        [first_name, last_name, username, password, ''],
        ['', last_name, username, password, password],
        [first_name, '', username, password, password],
        [first_name, last_name, '', password, password]
    ]

    @parameterized.expand(testdata)
    def test_invalid_form_without_requied_fields(self,
                                                 first_name,
                                                 last_name,
                                                 username,
                                                 password1,
                                                 password2):
        data = {'first_name': first_name,
                 'last_name': last_name,
                 'username': username,
                 'password1': password1,
                 'password2': password2}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
