from django.test import TestCase
from .models import Task
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class TaskAPITestCase(APITestCase):
    def setUp(self):

        # Create users
        self.user1 = User.objects.create_user(username='user1', password='testpass1')
        self.user2 = User.objects.create_user(username='user2', password='testpass2')

        # Create tasks for each user
        self.task1 = Task.objects.create(title='Task for user1', completed=False, user=self.user1)
        self.task2 = Task.objects.create(title='Task for user2', completed=True, user=self.user2)

        # Generate tokens
        self.user1_token = str(AccessToken.for_user(self.user1))
        self.user2_token = str(AccessToken.for_user(self.user2))

    def test_get_tasks_unauthorized(self):
        """ Verifying no unauthorized access to tasks.  """
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_tasks_authorized(self):
        """ Verifying creating tasks when authenticated. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        data = {
            'title': 'New task for user1',
            'completed': False
        }
        response = self.client.post('/api/tasks/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_get_tasks_user(self):
        """ Verifying getting tasks for a specific user. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task for user1')

    def test_get_filtered_task(self):
        """ Verifying filtering tasks by title. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.get('/api/tasks/', {'title': 'Task for user1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task for user1')

    def test_delete_task(self):
        """ Verifying deleting own task but not someone's task. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')

        user1_task_id = self.task1.id
        response = self.client.delete(f'/api/tasks/{user1_task_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=user1_task_id).exists())

        user2_task_id = self.task2.id
        response = self.client.delete(f'/api/tasks/{user2_task_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(id=user2_task_id).exists())

    def test_put_task(self):
        """ Verifying updating own task but not someone's task. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')

        user1_task_id = self.task1.id
        response = self.client.put(f'/api/tasks/{user1_task_id}/', {'title': 'Updated Task1', 'completed': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=user1_task_id)
        self.assertEqual(updated_task.title, 'Updated Task1')
        self.assertTrue(updated_task.completed)

        user2_task_id = self.task2.id
        response = self.client.put(f'/api/tasks/{user2_task_id}/', {'title': 'Updated Task2'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.get(id=user2_task_id).title == 'Task for user2')

    def test_patch_task(self):
        """ Verifying partial update of task. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', {'completed': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=self.task1.id)
        self.assertTrue(updated_task.completed)

    def test_create_task_missing_data(self):
        """ Verifying creation of task with missing data. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.post('/api/tasks/', {'completed': True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexisting_task(self):
        """ Verifying retrieval of non-existing task. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.get('/api/tasks/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_completion(self):
        """ Verifying filtering of tasks by completion status. """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.get('/api/tasks/', {'completed': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task for user1')
