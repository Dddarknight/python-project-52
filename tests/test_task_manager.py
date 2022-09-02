from django.test import TestCase
from task_manager.models import HexletUser
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
