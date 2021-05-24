from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

CREAT_USER_URL = reverse('user:register')
LOGIN_URL = reverse('user:login')
ME_URL = reverse('user:me')

u_payload = {
    'email': 'user@test.com',
    'username': 'testuser',
    'first_name': 'test',
    'password': '1234abcd',
    'gender': 'M',
}


def create_user(email=u_payload['email'], username=u_payload['username'],
                first_name=u_payload['first_name'], password=u_payload['password'],
                gender=u_payload['gender']):
    return get_user_model().objects. \
        create_user(email=email, username=username,
                    first_name=first_name, password=password,
                    gender=gender)


class TestPublicUserApi(TestCase):
    """Test public user api."""

    def setUp(self):
        self.client = APIClient()

    def test_create_new_user(self):
        """Test creating and returning new user."""
        res = self.client.post(CREAT_USER_URL, u_payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['first_name'], u_payload['first_name'])
        self.assertEqual(res.data['username'], u_payload['username'])
        self.assertEqual(res.data['email'], u_payload['email'])
        self.assertEqual(res.data['gender'], u_payload['gender'])
        user = get_user_model().objects.filter(username=u_payload['username'])[0]
        self.assertTrue(user.check_password(u_payload['password']))

    def test_create_invalid_user(self):
        """Test creating an invalid new user, should creatation not working."""
        payload = {
            'first_name': 'Ali',
            'email': 'ali@email.com',
            'password': 'testpass',
        }

        res = self.client.post(CREAT_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_too_short_password(self):
        """Test create a new user with to short password."""
        payload = {
            'first_name': 'Ali',
            'username': 'alawi',
            'email': 'ali@email.com',
            'password': '12',
        }
        res = self.client.post(CREAT_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_user_with_invalid_password(self):
        """Test create a new user with invalid password."""
        payload = {
            'first_name': 'Ali',
            'username': 'alawi',
            'email': 'ali@email.com',
            'password': '12345678',
        }
        res = self.client.post(CREAT_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_user_exist(self):
        """Test creating user that already exists fails."""

        # Create a new user with code.
        create_user()
        # Create a new user using same data with REST API.
        res = self.client.post(CREAT_USER_URL, u_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user_with_email(self):
        """Test creating a token for user when login."""
        create_user()

        res = self.client.post(LOGIN_URL, u_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_create_token_for_user_with_username(self):
        """Test creating a token for user when login."""
        payload = {
            # we use username keyword for username or email
            'username': 'alawi',
            'password': 'abcd1234',
        }
        create_user(username=payload['username'], password=payload['password'])

        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_create_token_invalid_credentials(self):
        "Test if that token is not created if invlide credentials are given."
        create_user(email='user@test.com', password='12345678')
        payload = {
            'first_name': 'test',
            'email': 'user@test.com',
            'password': '1234abcd',
        }
        res = self.client.post(LOGIN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that no token created when no user exists."""
        payload = {
            'first_name': 'test',
            'email': 'user@test.com',
            'password': '1234abcd',
        }
        res = self.client.post(LOGIN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required."""
        payload = {
            'email': 'user@test.com',
        }
        res = self.client.post(LOGIN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_no_user_data_when_login(self):
        """Test retrieve all user data when login."""
        payload = {
            'first_name': 'test',
            'password': '1234abcd',
            'email': 'user@test.com',
            'username': 'usertest',
        }

        create_user(**payload)

        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateUserApi(TestCase):
    """Test private user api."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieve profile for logged in used."""
        payload = {
            'email': self.user.email,
            'username': self.user.username,
            'first_name': self.user.first_name,
        }
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, res.data)

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url."""
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile."""
        payload = {
            'first_name': 'AB Test',
            'last_name': 'TOTO',
            'password': '123asdf'
        }

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertTrue(self.user.check_password(payload['password']))
