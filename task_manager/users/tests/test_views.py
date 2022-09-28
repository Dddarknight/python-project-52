from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy

from task_manager.users.models import HexletUser
from task_manager.utils import get_test_data
from task_manager.test_container import TestContainer


test_container = TestContainer()


class UserCreationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1_data = get_test_data('users.json')['users']['user1']
        cls.first_name = cls.user1_data['first_name']
        cls.last_name = cls.user1_data['last_name']
        cls.username = cls.user1_data['username']
        cls.password = cls.user1_data['password']

    def test_register_user(self):
        c = Client()
        data = {'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username,
                'password1': self.password,
                'password2': self.password}
        c.post('/users/create/', data)
        assert HexletUser.objects.get(id=1).first_name == (
            self.first_name)
        assert HexletUser.objects.get(id=1).last_name == (
            self.last_name)
        assert HexletUser.objects.get(id=1).username == (
            self.username)


class UserUpdateDeleteTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')
        cls.user1_data = get_test_data('users.json')['users']['user1']
        cls.user2_data = get_test_data('users.json')['users']['user2']
        cls.first_name = cls.user1_data['first_name']
        cls.last_name = cls.user1_data['last_name']
        cls.username = cls.user2_data['username']
        cls.password = cls.user1_data['password']

    def test_update_user(self):
        c = Client()
        c.force_login(self.user)
        new_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password1': self.password,
            'password2': self.password}
        c.post(f'/users/{self.user.id}/update/', new_data)
        assert HexletUser.objects.get(id=1).first_name == (
            self.first_name)
        assert HexletUser.objects.get(id=1).last_name == (
            self.last_name)
        assert HexletUser.objects.get(id=1).username == (
            self.username)

    def test_delete_user(self):
        c = Client()
        c.force_login(self.user)
        c.post(f'/users/{self.user.id}/delete/')
        users = []
        for user in HexletUser.objects.all():
            users.append(user)
        assert not users


class UserDeleteDeniedTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.task = test_container.create_task(
            'task1', cls.status, cls.user1, cls.user2)
        cls.user1_data = get_test_data('users.json')['users']['user1']
        cls.user2_data = get_test_data('users.json')['users']['user2']

    def test_delete_user_with_task(self):
        c = Client()
        user1_id = self.user1.id
        user2_id = self.user2.id
        c.force_login(self.user1)
        c.post(f'/users/{self.user1.id}/delete/')
        assert HexletUser.objects.get(id=user1_id).username == (
            self.user1_data['username'])
        c.force_login(self.user2)
        c.post(f'/users/{self.user2.id}/delete/')
        assert HexletUser.objects.get(id=user2_id).username == (
            self.user2_data['username'])


class UserViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')

    def test_create_view(self):
        c = Client()
        response = c.get(reverse_lazy('registration'))
        required_content_elements = [
            'Имя', 'Фамилия', 'Имя пользователя',
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и символы @/./+/-/_.',
            'Ваш пароль должен содержать как минимум 3 символа.',
            'Подтверждение пароля',
            'Для подтверждения введите, пожалуйста, пароль ещё раз.']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_update_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('update', args=['1']))
        required_content_elements = [
            'Имя', 'Фамилия', 'Имя пользователя',
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и символы @/./+/-/_.',
            'Ваш пароль должен содержать как минимум 3 символа.',
            'Подтверждение пароля',
            'Для подтверждения введите, пожалуйста, пароль ещё раз.']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_delete_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('delete', args=['1']))
        required_content_elements = [
            'Удаление пользователя',
            'Вы уверены, что хотите удалить John Black ?']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_users_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('users'))
        required_content_elements = [
            'ID', 'Имя пользователя', 'Полное имя', 'Дата создания',
            'Изменить', 'Удалить',
            '1', 'John Black', 'johnblack']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users.html')
        for element in required_content_elements:
            self.assertContains(response, element)
