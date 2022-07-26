from os import stat
from venv import create
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """
    Create a user with the given params, and return the created user.
    :return: A user object
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        """
        It creates a new client that will be used to make requests to the API
        """
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        We're creating a user with a valid payload, and then checking that the
        response is 201, and that the user exists in the database and if the
        password is not in the request object.
        """
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
            'name': 'test1'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', response.data)

    def test_user_exist(self):
        """
        We create a user with the payload, then we try to create another
        user with the same payload. We expect the second request to fail 
        because the email is already taken.
        """
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
            'name': 'test1'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        We're testing that if we try to create a user with a password that's
        too short, we get a 400 response and the user is not created
        """
        payload = {
            'email': 'test@gmail.com',
            'password': 'test',
            'name': 'test1'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()

        self.assertFalse(user_exists)

    def test_create_token_valid_user(self):
        """
        We're creating a user, then we're using the client to make a post
        request to the token url, and we're passing in the payload.

        Then, we're checking if in the request exist the auth token and the
        response status
        """
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass134',
            'name': 'test1'
        }
        create_user(**payload)

        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        We create a user, then we try to create a token with the wrong password
        """
        create_user(**{'email': 'test@gmail.com', 'password': 'testpass123'})
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrongpass',
            'name': 'test1'
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        We're testing that if we try to create a token with a user that doesn't exist, we get a 400 response
        """
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrongpass',
            'name': 'test1'
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_incomplete_fields(self):
        """
        We're testing that if we send a POST request to the token url with an incomplete payload, we should
        get a 400 response
        """
        payload = {
            'email': 'test@gmail.com',
            'name': 'test1'
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
