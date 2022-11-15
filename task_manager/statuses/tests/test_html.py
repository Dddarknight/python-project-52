from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep

from task_manager.statuses.models import Statuses
from task_manager.utils import get_test_data
from task_manager.test_container import TestContainer


test_container = TestContainer()


class StatusCreateTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = test_container.create_user('user1')
        cls.status1 = test_container.create_status('status1')
        cls.status1_data = (
            get_test_data('statuses.json')['statuses']['status1'])
        cls.name1 = cls.status1_data['name']
        cls.status2_data = (
            get_test_data('statuses.json')['statuses']['status2'])
        cls.name2 = cls.status2_data['name']

        cls.url_statuses = "/statuses/"
        cls.url_create = "/statuses/create"

        options = Options()
        options.headless = True
        cls.driver = webdriver.Firefox(options=options)

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {'name': 'sessionid',
             'value': cookie.value,
             'secure': False,
             'path': '/'}
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.delete_all_cookies()
        cls.driver.quit()
        super().tearDownClass()

    def test_create(self):
        self.driver.get('%s%s' % (self.live_server_url, self.url_statuses))
        try:
            create_link = self.driver.find_element(
                By.LINK_TEXT, 'Создать статус')
        except NoSuchElementException:
            create_link = self.driver.find_element(
                By.LINK_TEXT, 'Create status')
        create_link.click()
        sleep(1)

        name = self.driver.find_element(By.ID, 'id_name')
        name.send_keys(self.name1)
        self.driver.find_element(
            By.XPATH, "//form/input[@type='submit']").click()
        assert "Task status с таким Имя уже существует" in (
            self.driver.page_source
        ) or ("Task status with such Name already exists" in (
            self.driver.page_source))
        sleep(1)

        name = self.driver.find_element(By.ID, 'id_name')
        name.clear()
        name.send_keys(self.name2)
        self.driver.find_element(
            By.XPATH, "//form/input[@type='submit']").click()
        sleep(1)

        assert "Статус успешно создан" in (
            self.driver.page_source
        ) or ("Status created successfully" in (
            self.driver.page_source))

        self.driver.get('%s%s' % (self.live_server_url, self.url_statuses))
        sleep(1)
        assert self.name2 in self.driver.page_source


class StatusUpdateTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = test_container.create_user('user1')
        cls.status1 = test_container.create_status('status1')
        cls.status1_data = (
            get_test_data('statuses.json')['statuses']['status1'])
        cls.name1 = cls.status1_data['name']
        cls.status2_data = (
            get_test_data('statuses.json')['statuses']['status2'])
        cls.name2 = cls.status2_data['name']

        id = Statuses.objects.get(name=cls.name1).id
        cls.url_statuses = "/statuses/"
        cls.url_update = f"/statuses/{id}/update"

        options = Options()
        options.headless = True
        cls.driver = webdriver.Firefox(options=options)

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {'name': 'sessionid',
             'value': cookie.value,
             'secure': False,
             'path': '/'}
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.delete_all_cookies()
        cls.driver.quit()
        super().tearDownClass()

    def test_update(self):
        self.driver.get('%s%s' % (self.live_server_url, self.url_statuses))
        try:
            update_link = self.driver.find_element(By.LINK_TEXT, 'Изменить')
        except NoSuchElementException:
            update_link = self.driver.find_element(By.LINK_TEXT, 'Update')
        update_link.click()
        sleep(1)

        name = self.driver.find_element(By.ID, 'id_name')
        name.clear()
        name.send_keys(self.name2)
        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)

        assert "Статус успешно изменён" in (
            self.driver.page_source
        ) or ("Status updated successfully" in (
            self.driver.page_source))
        sleep(1)

        self.driver.get('%s%s' % (self.live_server_url, self.url_statuses))
        sleep(1)
        assert self.name2 in self.driver.page_source


class StatusDeleteTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = test_container.create_user('user1')
        cls.status1 = test_container.create_status('status1')
        cls.status1_data = (
            get_test_data('statuses.json')['statuses']['status1'])
        cls.name1 = cls.status1_data['name']

        id = Statuses.objects.get(name=cls.name1).id
        cls.url_statuses = "/statuses/"
        cls.url_delete = f"/statuses/{id}/delete"

        options = Options()
        options.headless = True
        cls.driver = webdriver.Firefox(options=options)

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {'name': 'sessionid',
             'value': cookie.value,
             'secure': False,
             'path': '/'}
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.delete_all_cookies()
        cls.driver.quit()
        super().tearDownClass()

    def test_delete(self):
        self.driver.get('%s%s' % (self.live_server_url, self.url_statuses))
        try:
            delete_link = self.driver.find_element(By.LINK_TEXT, 'Удалить')
        except NoSuchElementException:
            delete_link = self.driver.find_element(By.LINK_TEXT, 'Delete')
        delete_link.click()
        sleep(1)

        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)

        assert "Статус успешно удалён" in (
            self.driver.page_source
        ) or ("Status deleted successfully" in (
            self.driver.page_source))
        sleep(1)

        self.driver.get('%s%s' % (self.live_server_url, self.url_statuses))
        sleep(1)
        assert self.name1 not in self.driver.page_source
