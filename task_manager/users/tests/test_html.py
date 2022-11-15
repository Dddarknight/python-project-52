from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

from task_manager.utils import get_test_data
from task_manager.test_container import TestContainer


test_container = TestContainer()


class UsersTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1_data = get_test_data('users.json')['users']['user1']
        cls.first_name = cls.user1_data['first_name']
        cls.last_name = cls.user1_data['last_name']
        cls.username = cls.user1_data['username']
        cls.password = cls.user1_data['password']
        cls.url_sign_up = "/users/create"
        cls.url_users = "/users/"
        cls.url_login = "/login/"
        cls.url_logout = "/logout/"
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.delete_all_cookies()
        cls.driver.quit()
        super().tearDownClass()

    def test_sign_up_login_logout(self):
        self.driver.get('%s%s' % (self.live_server_url, self.url_sign_up))
        first_name = self.driver.find_element(By.ID, 'id_first_name')
        first_name.send_keys(self.first_name)
        last_name = self.driver.find_element(By.ID, 'id_last_name')
        last_name.send_keys(self.last_name)
        username = self.driver.find_element(By.ID, 'id_username')
        username.send_keys(self.username)
        password1 = self.driver.find_element(By.ID, 'id_password1')
        password1.send_keys(self.password)
        password2 = self.driver.find_element(By.ID, 'id_password2')
        password2.send_keys(self.password)
        self.driver.find_element(
            By.XPATH, "//form/input[@type='submit']").click()
        sleep(1)
        assert "Пользователь успешно зарегистрирован" in (
            self.driver.page_source)
        self.driver.get('%s%s' % (self.live_server_url, self.url_users))
        sleep(1)
        assert self.first_name in self.driver.page_source
        assert self.last_name in self.driver.page_source
        assert self.username in self.driver.page_source

        self.driver.get('%s%s' % (self.live_server_url, self.url_login))
        username = self.driver.find_element(By.ID, 'id_username')
        username.send_keys(self.username)
        password = self.driver.find_element(By.ID, 'id_password')
        password.send_keys(self.password)
        sleep(1)
        self.driver.find_element(
            By.XPATH, "//form/input[@type='submit']").click()
        sleep(1)
        assert "Вы залогинены" in self.driver.page_source
        expected_content_elements = ['Статусы', 'Метки', 'Задачи']
        for element in expected_content_elements:
            assert element in self.driver.page_source

        sleep(1)
        self.driver.get('%s%s' % (self.live_server_url, self.url_logout))
        sleep(1)
        assert "Вы разлогинены." in self.driver.page_source
        for element in expected_content_elements:
            assert element not in self.driver.page_source


class UsersUpdateTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = test_container.create_user('user1')
        cls.user1_data = get_test_data('users.json')['users']['user1']
        cls.first_name1 = cls.user1_data['first_name']
        cls.last_name1 = cls.user1_data['last_name']
        cls.username1 = cls.user1_data['username']
        cls.password1 = cls.user1_data['password']

        cls.user2_data = get_test_data('users.json')['users']['user2']
        cls.first_name2 = cls.user2_data['first_name']
        cls.last_name2 = cls.user2_data['last_name']
        cls.username2 = cls.user2_data['username']
        cls.password2 = cls.user2_data['password']

        id = get_user_model().objects.get(username=cls.username1).id
        cls.url_users = "/users/"
        cls.url_update = f"/users/{id}/update"

        cls.driver = webdriver.Firefox()

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})

    @classmethod
    def tearDownClass(cls):
        cls.driver.delete_all_cookies()
        cls.driver.quit()
        super().tearDownClass()

    def test_update(self):
        self.driver.get('%s%s' % (self.live_server_url, self.url_update))
        first_name = self.driver.find_element(By.ID, 'id_first_name')
        first_name.clear()
        first_name.send_keys(self.first_name2)
        last_name = self.driver.find_element(By.ID, 'id_last_name')
        last_name.clear()
        last_name.send_keys(self.last_name2)
        username = self.driver.find_element(By.ID, 'id_username')
        username.clear()
        username.send_keys(self.username2)
        password1 = self.driver.find_element(By.ID, 'id_password1')
        password1.send_keys(self.password2)
        password2 = self.driver.find_element(By.ID, 'id_password2')
        password2.send_keys(self.password2)
        sleep(2)
        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)
        assert "Пользователь успешно изменён" in (
            self.driver.page_source)

        self.driver.get('%s%s' % (self.live_server_url, self.url_users))
        sleep(1)
        assert self.first_name2 in self.driver.page_source
        assert self.first_name1 not in self.driver.page_source
        assert self.last_name2 in self.driver.page_source
        assert self.last_name1 not in self.driver.page_source
        assert self.username2 in self.driver.page_source
        assert self.username1 not in self.driver.page_source


class UsersDeleteTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = test_container.create_user('user1')
        cls.user1_data = get_test_data('users.json')['users']['user1']
        cls.first_name = cls.user1_data['first_name']
        cls.last_name = cls.user1_data['last_name']
        cls.username = cls.user1_data['username']
        cls.password = cls.user1_data['password']

        id = get_user_model().objects.get(username=cls.username).id
        cls.url_users = "/users/"
        cls.url_delete = f"/users/{id}/delete"

        cls.driver = webdriver.Firefox()

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})

    @classmethod
    def tearDownClass(cls):
        cls.driver.delete_all_cookies()
        cls.driver.quit()
        super().tearDownClass()

    def test_delete(self):
        self.driver.get('%s%s' % (self.live_server_url, self.url_delete))
        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)
        self.driver.get('%s%s' % (self.live_server_url, self.url_users))
        sleep(1)
        assert self.first_name not in self.driver.page_source
        assert self.last_name not in self.driver.page_source
        assert self.username not in self.driver.page_source
