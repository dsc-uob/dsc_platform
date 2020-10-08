from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from post_sys.tests import create_user, COMMENT_URL
from core.models import Post


class TestPublicCommentApi(TestCase):
    """Test of the public comment api."""

    def setUp(self):
        self.client = APIClient()

    def test_no_comment_unauthorized(self):
        """Test retrieve no post for unauthorized calls."""
        res = self.client.get(COMMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_create_comment_unauthorized(self):
        """Test can't create a new post in unauthorized calls."""
        post = Post.objects.create(
            title='Simple Title',
            body='This is simple body',
            user=create_user(),
        )

        payload = {
            'body': 'This is test post.',
            'post': post.id,
        }
        res = self.client.post(COMMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateCommentApi(TestCase):
    """Test of the private comment api."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.post = Post.objects.create(
            title='Simple Title',
            body='This is simple body',
            user=self.user,
        )

        self.client.force_authenticate(self.user)

    def test_get_all_comment(self):
        """Fetching all comments."""
        payload = {
            'body': 'This is simple comment.',
            'post': self.post.id,
        }
        self.client.post(COMMENT_URL, payload)

        payload = {
            'post': self.post.id,
        }

        res = self.client.get(COMMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_comment_successful(self):
        """Test creating and retrieving a new comment."""
        payload = {
            'body': 'This is simple comment.',
            'post': self.post.id,
        }

        res = self.client.post(COMMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['body'], payload['body'])
        self.assertEqual(res.data['user']['id'], self.user.id)

    def test_create_comment_invalid_body(self):
        """Test creating and retrieving a new comment."""
        payload = {
            'post': self.post.id,
        }

        res = self.client.post(COMMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_invalid_post(self):
        """Test creating and retrieving a new comment."""
        payload = {
            'body': 'This is simple comment.',
        }

        res = self.client.post(COMMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
