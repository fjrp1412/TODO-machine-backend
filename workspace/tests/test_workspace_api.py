from venv import create
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import User, Workspace
from workspace.serializers import WorkspaceSerializer

WORKSPACE_URL_LIST = reverse('workspace:workspace-list')


def create_user(**params):
    """
    Create a user with the given params, and return the created user.
    :return: A user object
    """
    return get_user_model().objects.create_user(**params)


class PublicWorkspaceApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        It tests that the `/workspace` endpoint returns a 401 status code when the user is not logged in
        """
        response = self.client.get(WORKSPACE_URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorkspaceApiTests(TestCase):
    def setUp(self):
        """
        It creates a user with the given email, password and name.
        """
        payload = {'email': 'test@gmail.com',
                   'password': 'testpass123', 'name': 'test 1'}
        self.client = APIClient()
        self.user = create_user(**payload)

        self.client.force_authenticate(self.user)

    def test_retrieve_user_workspace(self):
        """
        We create two workspaces, then we make a GET request to the WORKSPACE_URL endpoint, and we assert
        that the response is 200 OK and that the response data is equal to the serialized data of the
        workspaces we created
        """
        Workspace.objects.create(
            user=self.user, title='workspace test 1')

        Workspace.objects.create(
            user=self.user, title='workspace test 2'
        )

        response = self.client.get(WORKSPACE_URL_LIST)
        workspaces = Workspace.objects.all().order_by('-title')
        serializer = WorkspaceSerializer(workspaces, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_limited_user(self):
        """
        It creates a user, creates three workspaces, and then checks that the user can only see two of them
        """
        payload = {'email': 'test2@gmail.com', 'password': 'test123'}

        user2 = create_user(**payload)
        Workspace.objects.create(
            user=self.user, title='workspace test 1')

        Workspace.objects.create(
            user=self.user, title='workspace test 2'
        )
        Workspace.objects.create(
            user=user2, title='workspace test user 2'
        )

        response = self.client.get(WORKSPACE_URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_workspace(self):
        """
        We're creating a new workspace with a title and a user
        """
        payload = {
            'title': 'Workspace test 1',
            'user': self.user.pk
        }

        response = self.client.post(WORKSPACE_URL_LIST, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        exist = Workspace.objects.filter(
            user=self.user,
            title=payload['title']
        ).exists()

        self.assertTrue(exist)

    def test_create_workspace_invalid(self):
        """
        We're testing that if we send an empty title, we get a 400 response
        """
        payload = {
            'title': '',
            'user': self.user.id
        }

        response = self.client.post(WORKSPACE_URL_LIST, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_workpsace(self):
        """
        We create a new workspace, then we update it with a new title
        """
        new_workspace = Workspace.objects.create(
            user=self.user, title='workspace test 1')

        payload = {
            'title': 'updated title'
        }

        response = self.client.patch(
            reverse('workspace:workspace-detail', args=[new_workspace.pk]), payload)

        new_workspace.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_workspace.title)
        self.assertEqual(response.data['title'], payload['title'])

    def test_destroy_workspace(self):
        workspace = Workspace.objects.create(
            user=self.user, title='workspace test 1')

        response = self.client.delete(
            reverse('workspace:workspace-detail', args=[workspace.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        exist = Workspace.objects.filter(
            user=self.user,
            title=workspace.title
        ).exists()

        self.assertFalse(exist)
