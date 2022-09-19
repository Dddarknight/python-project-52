from django.test import TestCase
from task_manager.users.models import HexletUser
from django.test import Client
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation
from django.urls import reverse_lazy


test_container = TestObjectsCreation()


class UserTest(TestCase):
    test_data = get_test_data('users.json')

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
        c.force_login(user)
        new_data = {
            'first_name': (self.test_data['users']['user1']['first_name']),
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
        c.force_login(user)
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
        user = test_container.create_user1()
        c.force_login(user)
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
        user = test_container.create_user1()
        c.force_login(user)
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
        user = test_container.create_user1()
        c.force_login(user)
        response = c.get(reverse_lazy('users'))
        required_content_elements = [
            'ID', 'Имя пользователя', 'Полное имя', 'Дата создания',
            'Изменить', 'Удалить',
            '1', 'John Black', 'johnblack']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users.html')
        for element in required_content_elements:
            self.assertContains(response, element)
