from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Workspace


class WorkspaceModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com', password='testpass123', name='test1')

    def test_create_new_tag(self):
        """
        Create a new workspace with a title and user, and assert that the title and user are equal to the
        title and user that were passed in.
        """
        workspace = Workspace.objects.create(
            title='test title',
            user=self.user
        )

        self.assertEqual(workspace.title, 'test title')
        self.assertEqual(workspace.user, self.user)

    def test_str_workspace(self):
        workspace = Workspace.objects.create(
            title='test title',
            user=self.user
        )
        self.assertEqual(workspace.__str__(), 'test title')
