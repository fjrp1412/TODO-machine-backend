from django.test import TestCase
from django.contrib.auth import get_user_model


from core.models import Workspace, Todo

class TodoModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpass123',
            name='test1'
        )

        self.workspace = Workspace.objects.create(
            title='workspace test',
            user=self.user
        )
    
    def test_create_new_todo(self):
        todo = Todo.objects.create(
            title='todo test 1',
            user=self.user,
            workspace=self.workspace,
            description='description with too much text',
            priority='medium',
        )

        exist = Todo.objects.filter(
            title='todo test 1',
            id=todo.pk,
        ).exists()

        self.assertEqual(todo.user, self.user)
        self.assertEqual(todo.workspace, self.workspace)
        self.assertEqual(todo.title, 'todo test 1')
        self.assertTrue(exist)
