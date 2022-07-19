from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="testsuperuser@gmail.com",
            password="testpass123",
            name="Francisco Admin"
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="testuser@gmail.com",
            password="testpass123",
            name="Francisco User"
        )

    def test_users_listed(self):
        url = reverse("admin:core_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)
    
    def test_create_user_page(self):
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
