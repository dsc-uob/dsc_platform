from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from chat import tests as ct


class TestPublicChatSessionApi(TestCase):
    """Test the public api of chat session"""

    def setUp(self):
        self.client = APIClient()

    def test_get_chats_sessions_failed(self):
        """Test get all chats sessions unauthorized user."""
        res = self.client.get(
            ct.LIST_CHAT_SESSION_URL,
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_chat_session(self):
        """Test create a new chat session unauthorized user."""
        payload = {
            "add_members": [1],
            "title": "General",
        }
        res = self.client.post(
            ct.CREATE_CHAT_SESSION_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateChatSessionApi(TestCase):
    """Test the private api of chat session"""

    def setUp(self):
        self.client = APIClient()
        self.user = ct.create_user()

        self.client.force_authenticate(user=self.user)

    def test_get_my_chats_sessions_success(self):
        """Test get all chats sessions success."""
        # Create a new chat session for user2
        user2 = ct.create_user(
            email='user2@test.com',
            username='test2'
        )
        payload2 = {
            "add_members": [user2.id],
            "title": "General2",
        }
        client = APIClient()
        client.force_authenticate(user2)
        client.post(
            ct.CREATE_CHAT_SESSION_URL,
            payload2
        )

        # Create chat session of user
        payload = {
            "add_members": [self.user.id, user2.id],
            "title": "General",
        }
        self.client.post(
            ct.CREATE_CHAT_SESSION_URL,
            payload
        )

        # Check user
        res = self.client.get(
            ct.LIST_CHAT_SESSION_URL,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

        # Check user2
        res2 = client.get(
            ct.LIST_CHAT_SESSION_URL,
        )
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data['count'], 2)

    def test_create_chat_session_success(self):
        """Test create a chat session successful."""
        payload = {
            "add_members": [self.user.id, ],
            "title": "General",
        }
        res = self.client.post(
            ct.CREATE_CHAT_SESSION_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(res.data['members']), len(payload['add_members']))
        self.assertEqual(res.data['title'], payload['title'])

    def test_create_chat_session_invalid_title(self):
        """Test create a new chat session with no title"""
        payload = {
            "add_members": [self.user.id, ],
        }
        res = self.client.post(
            ct.CREATE_CHAT_SESSION_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
