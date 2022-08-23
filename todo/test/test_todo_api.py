from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from todo.serializers import TodoSerializer

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
        """
        We create a new user and a new workspace, then we create a new todo for that user and workspace.
        Then we create two more todos for the original user and workspace. Then we make a GET request to the
        workspace list endpoint and assert that the response data contains only the two todos for the
        original user and workspace
        """
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

        response = self.client.get(TODO_URL_LIST)
        todos = models.Todo.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(len(todos), 3)

    def test_retrieve_todos_for_given_workspace(self):
        """
        We create a new workspace, then create 3 todos, 2 of which are assigned to the first workspace, and
        1 to the second. 

        Then we make a GET request to the todo list endpoint, passing in the first workspace's pk as a query
        parameter. 

        We assert that the response status code is 200, that the length of the response data is 2, and that
        the first item in the response data has the first workspace's pk as its workspace.
        """

        workspace2 = models.Workspace.objects.create(
            user=self.user, title='workspace test 2')

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
            user=self.user,
            workspace=workspace2,
            description='Test todo description',
            priority='low'
        )

        response = self.client.get(
            f'{TODO_URL_LIST}?workspace={self.workspace.pk}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['workspace'], self.workspace.pk)

    def test_edit_todo(self):
        """
        We create a todo, then we update it and check that the response is 200 and that the data is not the
        same as the payload
        """
        payload = {
            'title': 'test todo',
            'user': self.user,
            'workspace': self.workspace,
            'priority': 'low',
            'description': 'descripcion',
        }
        todo_test = models.Todo.objects.create(**payload)

        response = self.client.patch(reverse('todo:todo-detail',
                                             args=[todo_test.pk]), {'title': 'test todo updated'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, payload)

    def test_destroy_todo(self):
        """
        We create a todo, then we delete it and check that it doesn't exist anymore
        """
        payload = {
            'title': 'test todo',
            'user': self.user,
            'workspace': self.workspace,
            'priority': 'low',
            'description': 'descripcion',
        }

        todo_test = models.Todo.objects.create(**payload)

        response = self.client.delete(
            reverse('todo:todo-detail', args=[todo_test.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        exist = models.Todo.objects.filter(id=todo_test.pk).exists()

        self.assertFalse(exist)
