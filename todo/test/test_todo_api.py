from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from todo.serializers import TodoSerializer
from workspace.tests.test_workspace_api import WORKSPACE_URL_LIST

TODO_URL_LIST = reverse('todo:todo-list')


def create_user(**params):
    """
    Create a user with the given params, and return the created user.
    :return: A user object
    """
    return models.User.objects.create_user(**params)


class PublicTodoApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        response = self.client.get(TODO_URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoApiTests(TestCase):

    def setUp(self):
        """
        We create a user, a workspace, and then authenticate the user
        """
        self.client = APIClient()
        self.user = create_user(
            **{'email': 'test@gmail.com',
               'password': 'testpass123',
               'name': 'test'})
        self.workspace = models.Workspace.objects.create(
            title='workspace test 1',
            user=self.user,
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_user_todos(self):
        """
        We create a todo, then we make a GET request to the todo list endpoint, then we check if the
        response is 200 and if the response data is equal to the serialized data.
        """
        payload = {
            'title': 'Test todo 1',
            'user': self.user,
            'workspace': self.workspace,
            'description': 'Test TODO description',
            'priority': 'medium',
        }

        models.Todo.objects.create(**payload)
        response = self.client.get(TODO_URL_LIST)
        todos = models.Todo.objects.all().order_by('-title')
        serializer = TodoSerializer(todos, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_limited_user(self):
        payload = {'email': 'test2@gmail.com', 'password': 'testpass123'}

        user2 = create_user(**payload)
        workspace2 = models.Workspace.objects.create(
            user=user2, title='workspace test 2')

        models.Todo.objects.create(
            title='Test todo 1',
            user=self.user,
            workspace=self.workspace,
            description='Test todo description',
            priority='low'
        )

        models.Todo.objects.create(
            title='Test todo 2',
            user=self.user,
            workspace=self.workspace,
            description='Test todo description',
            priority='low'
        )

        models.Todo.objects.create(
            title='Test todo 2',
            user=user2,
            workspace=workspace2,
            description='Test todo description',
            priority='low'
        )

        response = self.client.get(WORKSPACE_URL_LIST)
        todos = models.Todo.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(len(todos), 4)
