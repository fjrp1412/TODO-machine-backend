from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        """
        We create a user with an email and password, then we assert that the user's email is equal to the
        email we passed in, and that the user's password is equal to the password we passed in
        """

        email = "test@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        We create a user with an email address that has uppercase letters, and then we check that the email
        address is normalized to all lowercase letters
        """
        email = "test@GMAIL.COM"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        We're testing that if we try to create a user with no email, we get a ValueError
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="testpass123"
            )

    def test_create_new_superuser(self):
        """
        We create a new user with the create_superuser function, and then we assert that the user is a
        superuser and a staff user
        """
        email = "test@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
