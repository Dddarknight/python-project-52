from django.test import Client
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.labels.models import Labels
from task_manager.test_container import TestContainer
from task_manager.utils import get_test_data


test_container = TestContainer()


class LabelCreationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.label1_data = (
            get_test_data('labels.json')['labels']['label1'])
        cls.name = cls.label1_data['name']
        cls.user1 = test_container.create_user('user1')

    def test_create_label(self):
        c = Client()
        c.force_login(self.user1)
        label_data = {'name': self.name}
        c.post('/labels/create/', label_data)
        assert Labels.objects.get(id=1).name == (
            self.name)


class LabelUpdateDeleteTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = test_container.create_user('user1')
        cls.label1 = test_container.create_label('label1')
        cls.label2 = test_container.create_label('label2')
        cls.label1_data = (
            get_test_data('labels.json')['labels']['label1'])
        cls.name1 = cls.label1_data['name']
        cls.label2_data = (
            get_test_data('labels.json')['labels']['label2'])
        cls.name2 = cls.label2_data['name']
        cls.label3_data = (
            get_test_data('labels.json')['labels']['label3'])
        cls.name3 = cls.label3_data['name']

    def test_update_label(self):
        c = Client()
        c.force_login(self.user1)
        new_data_invalid = {'name': self.name2}
        c.post(f'/labels/{self.label1.id}/update/', new_data_invalid)
        assert Labels.objects.get(id=self.label1.id).name == self.name1
        new_data_valid = {'name': self.name3}
        c.post(f'/labels/{self.label1.id}/update/', new_data_valid)
        assert Labels.objects.get(id=self.label1.id).name == (
            self.name3)

    def test_delete_label(self):
        c = Client()
        c.force_login(self.user1)
        c.post(f'/labels/{self.label1.id}/delete/')
        c.post(f'/labels/{self.label2.id}/delete/')
        labels = []
        for label in Labels.objects.all():
            labels.append(label)
        assert not labels


class LabelDeleteDeniedTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = test_container.create_user('user1')
        cls.user2 = test_container.create_user('user2')
        cls.status = test_container.create_status('status1')
        cls.label1 = test_container.create_label('label1')
        cls.label2 = test_container.create_label('label2')
        cls.task1 = test_container.create_task(
            'task1', cls.status, cls.user1, cls.user2)
        cls.task1.labels.add(cls.label1)
        cls.task1.labels.add(cls.label2)
        cls.label1_data = (
            get_test_data('labels.json')['labels']['label1'])
        cls.name = cls.label1_data['name']

    def test_delete_label_with_task(self):
        c = Client()
        label1_id = self.label1.id
        c.force_login(self.user1)
        c.post(f'/labels/{self.label1.id}/delete/')
        assert Labels.objects.get(id=label1_id).name == self.name


class LabelViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = test_container.create_user('user1')
        cls.label = test_container.create_label('label1')

    def test_create_view(self):
        c = Client()
        response = c.get(reverse_lazy('label_create'))
        required_content_elements = ['Имя']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_create.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_update_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('label_update', args=['1']))
        required_content_elements = ['Имя']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_update.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_delete_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('label_delete', args=['1']))
        required_content_elements = [
            'Удаление метки',
            'Вы уверены, что хотите удалить label1 ?']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_delete.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_labels_view(self):
        c = Client()
        c.force_login(self.user)
        response = c.get(reverse_lazy('labels'))
        required_content_elements = [
            'ID', 'Имя', 'Дата создания',
            'Изменить', 'Удалить',
            '1', 'label1']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/labels.html')
        for element in required_content_elements:
            self.assertContains(response, element)
