from django.test import TestCase
from task_manager.labels.models import Labels
from django.test import Client
from task_manager.utils import get_test_data
from task_manager.tests import TestObjectsCreation
from django.urls import reverse_lazy


test_container = TestObjectsCreation()


class LabelTest(TestCase):
    test_data = get_test_data('labels.json')

    def test_create_label(self):
        c = Client()
        user1 = test_container.create_user1()
        c.force_login(user1)
        label_data = {'name': self.test_data['labels']['label1']['name']}
        c.post('/labels/create/', label_data)
        assert Labels.objects.get(id=1).name == (
            self.test_data['labels']['label1']['name'])

    def test_update_label(self):
        c = Client()
        user1 = test_container.create_user1()
        c.force_login(user1)
        label1 = test_container.create_label1()
        test_container.create_label2()
        new_data_invalid = {'name': self.test_data['labels']['label2']['name']}
        c.post(f'/labels/{label1.id}/update/', new_data_invalid)
        assert Labels.objects.get(id=label1.id).name == (
            self.test_data['labels']['label1']['name'])
        new_data_valid = {'name': self.test_data['labels']['label3']['name']}
        c.post(f'/labels/{label1.id}/update/', new_data_valid)
        assert Labels.objects.get(id=label1.id).name == (
            self.test_data['labels']['label3']['name'])

    def test_delete_label(self):
        c = Client()
        user1 = test_container.create_user1()
        label1 = test_container.create_label1()
        c.force_login(user1)
        c.post(f'/labels/{label1.id}/delete/')
        labels = []
        for label in Labels.objects.all():
            labels.append(label)
        assert not labels

    def test_delete_label_with_task(self):
        c = Client()
        user1 = test_container.create_user1()
        user2 = test_container.create_user2()
        status = test_container.create_status1()
        label1 = test_container.create_label1()
        label1_id = label1.id
        label2 = test_container.create_label2()
        task = test_container.create_task1(status, user1, user2)
        task.labels.add(label1)
        task.labels.add(label2)
        c.force_login(user1)
        c.post(f'/labels/{label1.id}/delete/')
        assert Labels.objects.get(id=label1_id).name == "label1"

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
        user = test_container.create_user1()
        c.force_login(user)
        test_container.create_label1()
        response = c.get(reverse_lazy('label_update', args=['1']))
        required_content_elements = ['Имя']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_update.html')
        for element in required_content_elements:
            self.assertContains(response, element)

    def test_delete_view(self):
        c = Client()
        user = test_container.create_user1()
        c.force_login(user)
        test_container.create_label1()
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
        user = test_container.create_user1()
        c.force_login(user)
        test_container.create_label1()
        response = c.get(reverse_lazy('labels'))
        required_content_elements = [
            'ID', 'Имя', 'Дата создания',
            'Изменить', 'Удалить',
            '1', 'label1']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/labels.html')
        for element in required_content_elements:
            self.assertContains(response, element)
