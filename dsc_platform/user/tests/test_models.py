from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

data = {
    'email': 'user@test.com',
    'inv_email': 'email',
    'username': 'test',
    'inv_username': 'test@user',
    'first_name': 'Ali',
    'password': 'password1234',
    'birth_date': '2000-10-10',
}


def create_user(email='user@test.com', username='testuser',
                first_name='test', password='1234abcd'):
    return get_user_model().objects. \
        create_user(email=email, username=username,
                    first_name=first_name, password=password)


class TestUserModel(TestCase):
    """
    A test for user model
    """

    def test_create_user(self):
        """Test creating and returning a new user."""
        user_data = {
            'email': 'user@test.com',
            'username': 'test_user',
            'first_name': 'Ali',
            'password': 'password1234',
            'birth_date': '2000-10-10',
        }

        user = get_user_model().objects.create_user(
            email=user_data['email'],
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            birth_date=user_data['birth_date']
        )
        self.assertEqual(user.email, user_data['email'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.username, user_data['username'])
        self.assertTrue(user.check_password(user_data['password']))
        self.assertTrue(user.birth_date, user_data['birth_date'])

    def test_create_user_with_invalid_username_data(self):
        """Test create user with invalid username."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=data['email'],
                username=data['inv_username'],
                password=data['password'],
                first_name=data['first_name'],
            )

    def test_create_user_with_no_username(self):
        """Test creating user with no username."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=data['email'],
                username=None,
                password=data['password'],
                first_name=data['first_name'],
            )

    def test_create_user_with_no_email(self):
        """Test creating user with no email."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                username=data['username'],
                password=data['password'],
                first_name=data['first_name'],
            )

    def test_creating_user_normalize(self):
        """Test Creating a normalize email address for a new user."""
        user = get_user_model().objects.create_user(
            email=data['email'],
            password=data['password'],
            username=data['username'],
            first_name=data['first_name'],
            birth_date=data['birth_date'],
        )

        self.assertEqual(user.email, data['email'].lower())
        self.assertTrue(user.check_password(data['password']))

    def test_creating_superuser(self):
        """Test creating a new superuser."""

        user = get_user_model().objects.create_superuser(
            email=data['email'],
            password=data['password'],
            username=data['username'],
            first_name=data['first_name'],
            birth_date=data['birth_date'],

        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
