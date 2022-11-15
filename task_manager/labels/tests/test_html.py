from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep

from task_manager.labels.models import Labels
from task_manager.utils import get_test_data
from task_manager.test_container import TestContainer


test_container = TestContainer()


class LabelCreateTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = test_container.create_user('user1')
        cls.label1 = test_container.create_label('label1')
        cls.label1_data = (
            get_test_data('labels.json')['labels']['label1'])
        cls.name1 = cls.label1_data['name']
        cls.label2_data = (
            get_test_data('labels.json')['labels']['label2'])
        cls.name2 = cls.label2_data['name']

        cls.url_labels = "/labels/"
        cls.url_create = "/labels/create"

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
        self.driver.get('%s%s' % (self.live_server_url, self.url_labels))
        try:
            create_link = self.driver.find_element(
                By.LINK_TEXT, 'Создать метку')
        except NoSuchElementException:
            create_link = self.driver.find_element(
                By.LINK_TEXT, 'Create label')
        create_link.click()
        sleep(1)

        name = self.driver.find_element(By.ID, 'id_name')
        name.send_keys(self.name1)
        self.driver.find_element(
            By.XPATH, "//form/input[@type='submit']").click()
        assert "Label с таким Имя уже существует" in (
            self.driver.page_source
        ) or ("Label with such Name already exists" in (
            self.driver.page_source))
        sleep(1)

        name = self.driver.find_element(By.ID, 'id_name')
        name.clear()
        name.send_keys(self.name2)
        self.driver.find_element(
            By.XPATH, "//form/input[@type='submit']").click()
        sleep(1)

        assert "Метка успешно создана" in (
            self.driver.page_source
        ) or ("Label created successfully" in (
            self.driver.page_source))

        self.driver.get('%s%s' % (self.live_server_url, self.url_labels))
        sleep(1)
        assert self.name2 in self.driver.page_source


class LabelUpdateTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = test_container.create_user('user1')
        cls.label1 = test_container.create_label('label1')
        cls.label1_data = (
            get_test_data('labels.json')['labels']['label1'])
        cls.name1 = cls.label1_data['name']
        cls.label2_data = (
            get_test_data('labels.json')['labels']['label2'])
        cls.name2 = cls.label2_data['name']

        id = Labels.objects.get(name=cls.name1).id
        cls.url_labels = "/labels/"
        cls.url_update = f"/labels/{id}/update"

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
        self.driver.get('%s%s' % (self.live_server_url, self.url_labels))
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

        assert "Метка успешно изменена" in (
            self.driver.page_source
        ) or ("Label updated successfully" in (
            self.driver.page_source))
        sleep(1)

        self.driver.get('%s%s' % (self.live_server_url, self.url_labels))
        sleep(1)
        assert self.name2 in self.driver.page_source


class LabelDeleteTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = test_container.create_user('user1')
        cls.label1 = test_container.create_label('label1')
        cls.label1_data = (
            get_test_data('labels.json')['labels']['label1'])
        cls.name1 = cls.label1_data['name']

        id = Labels.objects.get(name=cls.name1).id
        cls.url_labels = "/labels/"
        cls.url_delete = f"/labels/{id}/delete"

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
        self.driver.get('%s%s' % (self.live_server_url, self.url_labels))
        try:
            delete_link = self.driver.find_element(By.LINK_TEXT, 'Удалить')
        except NoSuchElementException:
            delete_link = self.driver.find_element(By.LINK_TEXT, 'Delete')
        delete_link.click()
        sleep(1)

        self.driver.find_element(
            By.XPATH, "//form/button[@type='submit']").click()
        sleep(1)

        assert "Метка успешно удалена" in (
            self.driver.page_source
        ) or ("Label deleted successfully" in (
            self.driver.page_source))
        sleep(1)

        self.driver.get('%s%s' % (self.live_server_url, self.url_labels))
        sleep(1)
        assert self.name1 not in self.driver.page_source
