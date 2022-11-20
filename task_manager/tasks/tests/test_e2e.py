from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from time import sleep

from task_manager.statuses.models import Statuses
from task_manager.utils import get_test_data
from task_manager.test_container import TestContainer


test_container = TestContainer()


class TaskCreateTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.task1_data = (
            get_test_data('tasks.json')['tasks']['task1'])
        cls.name1 = cls.task1_data['name']
        cls.task1 = test_container.create_task(
            cls.name1, cls.status, cls.user1, cls.user2)
        cls.task2_data = (
            get_test_data('tasks.json')['tasks']['task2'])
        cls.name2 = cls.task2_data['name']
        cls.description2 = cls.task2_data['description']
        cls.label1 = test_container.create_label('label1')
        cls.label2 = test_container.create_label('label2')

        cls.url_tasks = "/tasks/"
        cls.url_create = "/tasks/create"

        options = Options()
        options.headless = True
        cls.driver = webdriver.Firefox(options=options)

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user1)
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
        self.driver.get('%s%s' % (self.live_server_url, self.url_tasks))
        try:
            create_link = self.driver.find_element(
                By.LINK_TEXT, 'Создать задачу')
        except NoSuchElementException:
            create_link = self.driver.find_element(By.LINK_TEXT, 'Create task')
        create_link.click()
        sleep(1)

        name = self.driver.find_element(By.ID, 'id_name')
        name.send_keys(self.name1)
        description = self.driver.find_element(By.ID, 'id_description')
        description.send_keys(self.description2)
        select_status = Select(self.driver.find_element(By.ID, 'id_status'))
        select_status.select_by_visible_text('status1')
        select_executor = Select(
            self.driver.find_element(By.ID, 'id_executor'))
        select_executor.select_by_visible_text('John Black')
        select_labels = Select(self.driver.find_element(By.ID, 'id_labels'))
        select_labels.select_by_visible_text('label1')
        select_labels.select_by_visible_text('label2')
        self.driver.find_element(
            By.XPATH, "//form/input[@type='submit']").click()
        assert "Task с таким Имя уже существует" in (
            self.driver.page_source
        ) or ("Task with such Name already exists" in (
            self.driver.page_source))
        sleep(1)

        name = self.driver.find_element(By.ID, 'id_name')
        name.clear()
        name.send_keys(self.name2)
        self.driver.find_element(
            By.XPATH, "//form/input[@type='submit']").click()
        sleep(1)

        assert "Задача успешно создана" in (
            self.driver.page_source
        ) or ("Task created successfully" in (
            self.driver.page_source))

        self.driver.get('%s%s' % (self.live_server_url, self.url_tasks))
        sleep(1)
        assert self.name2 in self.driver.page_source


class TaskUpdateTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.task1_data = (
            get_test_data('tasks.json')['tasks']['task1'])
        cls.name1 = cls.task1_data['name']
        cls.description1 = cls.task1_data['description']
        cls.task1 = test_container.create_task(
            cls.name1, cls.status, cls.user1, cls.user1)
        cls.task2_data = (
            get_test_data('tasks.json')['tasks']['task2'])
        cls.name2 = cls.task2_data['name']
        cls.description2 = cls.task2_data['description']
        cls.label1 = test_container.create_label('label1')
        cls.label2 = test_container.create_label('label2')

        cls.url_tasks = "/tasks/"

        options = Options()
        options.headless = True
        cls.driver = webdriver.Firefox(options=options)

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user1)
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
        self.driver.get('%s%s' % (self.live_server_url, self.url_tasks))
        try:
            update_link = self.driver.find_element(
                By.LINK_TEXT, 'Изменить')
        except NoSuchElementException:
            update_link = self.driver.find_element(By.LINK_TEXT, 'Update')
        update_link.click()
        sleep(1)

        name = self.driver.find_element(By.ID, 'id_name')
        name.clear()
        name.send_keys(self.name2)
        description = self.driver.find_element(By.ID, 'id_description')
        description.clear()
        description.send_keys(self.description2)
        select_executor = Select(
            self.driver.find_element(By.ID, 'id_executor'))
        select_executor.select_by_visible_text('Bob Green')
        select_labels = Select(self.driver.find_element(By.ID, 'id_labels'))
        select_labels.select_by_visible_text('label1')
        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)

        assert "Задача успешно изменена" in (
            self.driver.page_source
        ) or ("Task updated successfully" in (
            self.driver.page_source))

        self.driver.get('%s%s' % (self.live_server_url, self.url_tasks))
        sleep(1)
        assert self.name1 not in self.driver.page_source
        assert self.name2 in self.driver.page_source
        assert self.user2.first_name in self.driver.page_source
        assert self.user2.last_name in self.driver.page_source

        description_link = self.driver.find_element(
            By.LINK_TEXT, self.name2)
        description_link.click()
        sleep(1)
        assert self.description1 not in self.driver.page_source
        assert self.description2 in self.driver.page_source
        assert self.label1.name in self.driver.page_source
        assert self.label2.name not in self.driver.page_source


class TaskDeleteTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.task1_data = (
            get_test_data('tasks.json')['tasks']['task1'])
        cls.name1 = cls.task1_data['name']
        cls.description1 = cls.task1_data['description']
        cls.task1 = test_container.create_task(
            cls.name1, cls.status, cls.user1, cls.user2)

        cls.url_tasks = "/tasks/"

        options = Options()
        options.headless = True
        cls.driver = webdriver.Firefox(options=options)

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user1)
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
        self.driver.get('%s%s' % (self.live_server_url, self.url_tasks))
        try:
            delete_link = self.driver.find_element(
                By.LINK_TEXT, 'Удалить')
        except NoSuchElementException:
            delete_link = self.driver.find_element(By.LINK_TEXT, 'Delete')
        delete_link.click()
        sleep(1)

        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)

        assert "Задача успешно удалена" in (
            self.driver.page_source
        ) or ("Task deleted successfully" in (
            self.driver.page_source))

        self.driver.get('%s%s' % (self.live_server_url, self.url_tasks))
        sleep(1)
        assert self.name1 not in self.driver.page_source


class TaskInvalidDeleteTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.task1_data = (
            get_test_data('tasks.json')['tasks']['task1'])
        cls.name1 = cls.task1_data['name']
        cls.description1 = cls.task1_data['description']
        cls.task1 = test_container.create_task(
            cls.name1, cls.status, cls.user1, cls.user2)

        cls.url_tasks = "/tasks/"
        user_id = get_user_model().objects.get(username=cls.user2.username).id
        cls.url_user = f"/users/{user_id}/delete"
        status_id = Statuses.objects.get(name=cls.status.name).id
        cls.url_status = f"/statuses/{status_id}/delete"

        options = Options()
        options.headless = True
        cls.driver = webdriver.Firefox(options=options)

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user2)
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
        self.driver.get('%s%s' % (self.live_server_url, self.url_tasks))
        try:
            delete_link = self.driver.find_element(
                By.LINK_TEXT, 'Удалить')
        except NoSuchElementException:
            delete_link = self.driver.find_element(By.LINK_TEXT, 'Delete')
        delete_link.click()
        sleep(1)

        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)

        assert "Задачу может удалить только её автор." in (
            self.driver.page_source
        ) or ("Task can be deleted only by the author." in (
            self.driver.page_source))

        self.driver.get('%s%s' % (self.live_server_url, self.url_tasks))
        sleep(1)
        assert self.name1 in self.driver.page_source

        self.driver.get('%s%s' % (self.live_server_url, self.url_user))
        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)
        assert ("Невозможно удалить пользователя, "
                "потому что он используется") in (
            self.driver.page_source
        ) or ("Cannot delete user because it is in use" in (
            self.driver.page_source))

        self.driver.get('%s%s' % (self.live_server_url, self.url_status))
        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)
        assert "Невозможно удалить статус, потому что он используется" in (
            self.driver.page_source
        ) or ("Cannot delete status because it is in use" in (
            self.driver.page_source))
