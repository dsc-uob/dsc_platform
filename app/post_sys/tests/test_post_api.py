from post_sys.tests import create_user, POSTS_URL

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status


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

    def test_create_invalid_post_title(self):
        """Testing creating an invalid post."""
        payload = {
            'body': 'This is simple post.',
        }

        res = self.client.post(POSTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_post_body(self):
        """Testing creating an invalid post."""
        payload = {
            'title': 'Simple title.',
        }

        res = self.client.post(POSTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_posts(self):
        """Test get all user posts"""
        user2 = create_user(email='user2@test.com', username='Test2')
        client = APIClient()
        client.force_authenticate(user=user2)

        payload = {
            'title': 'This is a title',
            'body': 'This is a body',
        }

        self.client.post(POSTS_URL, payload)
        client.post(POSTS_URL, payload)
        res = self.client.get(POSTS_URL, {'user': self.user.id})

        self.assertEqual(res.data['count'], 1)
        self.assertEqual(res.data['results'][0]['title'], payload['title'])
        self.assertEqual(res.data['results'][0]['body'], payload['body'])
