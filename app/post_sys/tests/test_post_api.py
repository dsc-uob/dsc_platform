from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

POSTS_URL = reverse('post_sys:post-list')


def create_user(email='user@test.com', username='testuser',
                first_name='test', password='1234abcd'):
    return get_user_model().objects. \
        create_user(email=email, username=username,
                    first_name=first_name, password=password)


class TestPublicPostApi(TestCase):
    """Test of the public post api."""

    def setUp(self):
        self.client = APIClient()

    def test_no_post_unauthorized(self):
        """Test retrieve no post for unauthorized calls."""
        res = self.client.get(POSTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_create_post_unauthorized(self):
        """Test can't create a new post in unauthorized calls."""
        payload = {
            'title': 'Simple title.',
            'body': 'This is test post.'
        }
        res = self.client.post(POSTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivatePostApi(TestCase):
    """Test of the private post api"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_get_posts_successful(self):
        """Test retrieve no post for unauthorized calls."""
        res = self.client.get(POSTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_post_successful(self):
        """Test creating and retrieving a new post."""
        payload = {
            'title': 'Simple title.',
            'body': 'This is simple post.',
        }

        res = self.client.post(POSTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['body'], payload['body'])
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['user']['id'], self.user.id)

    def test_create_invalid_post(self):
        """Testing creating an invalid post."""
        payload = {
            'body': 'This is simple post.',
        }

        res = self.client.post(POSTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
