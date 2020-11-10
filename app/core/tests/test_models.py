from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import utils
from core.models import Post, Comment, ChatSession, \
    ChatMessage, ChatMember, ChatRole

data = {
    'email': 'user@test.com',
    'inv_email': 'email',
    'username': 'test',
    'inv_username': 'test@user',
    'first_name': 'Ali',
    'password': 'password1234',
}


def create_user(email='user@test.com', username='testuser',
                first_name='test', password='1234abcd'):
    return get_user_model().objects. \
        create_user(email=email, username=username,
                    first_name=first_name, password=password)


class TestUserModel(TestCase):
    """Test user model"""

    def test_create_user(self):
        """Test creating and returning a new user."""
        user_data = {
            'email': 'user@test.com',
            'username': 'test_user',
            'first_name': 'Ali',
            'password': 'password1234',
        }

        user = get_user_model().objects.create_user(
            email=user_data['email'],
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
        )
        self.assertEqual(user.email, user_data['email'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.username, user_data['username'])
        self.assertTrue(user.check_password(user_data['password']))

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
            first_name=data['first_name']
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
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    @patch('uuid.uuid4')
    def test_user_photo_file_name_uuid(self, mock_uuid):
        """Test that image saved in the correct location."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = utils.user_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/user/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)


class TestPostModel(TestCase):
    """Test class for posts."""

    def setUp(self):
        self.user = create_user()

    def test_create_post_success(self):
        """Test creating and retrieving a new post."""
        payload = {
            'title': 'Post Title',
            'body': 'Test Body',
        }
        post = Post.objects.create(
            user=self.user,
            title=payload['title'],
            body=payload['body'],
        )

        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.body, payload['body'])
        self.assertEqual(post.user, self.user)

    def test_create_post_invalid_user(self):
        """Test creating a new post with no user."""
        with self.assertRaises(Exception):
            payload = {
                'title': 'Post Title',
                'body': 'Test Body',
            }
            Post.objects.create(
                title=payload['title'],
                body=payload['body'],
            )


class TestCommentModel(TestCase):
    """Test class for comments."""

    def setUp(self):
        self.user = create_user()
        payload = {
            'title': 'Post Title',
            'body': 'Test Body',
        }
        self.post = Post.objects.create(
            user=self.user,
            title=payload['title'],
            body=payload['body'],
        )

    def test_create_comment_success(self):
        """Test creating and retrieving comment."""
        payload = {
            'body': 'Test Body',
        }
        comment = Comment.objects.create(
            user=self.user,
            body=payload['body'],
            post=self.post,
        )

        self.assertEqual(comment.body, payload['body'])
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)

    def test_create_comment_invalid_user(self):
        """Test creating a new comment with no user."""
        with self.assertRaises(Exception):
            payload = {
                'body': 'Test Body',
            }
            Comment.objects.create(
                body=payload['body'],
                post=self.post,
            )

    def test_create_comment_invalid_post(self):
        """Test creating a new comment with no user."""
        with self.assertRaises(Exception):
            payload = {
                'body': 'Test Body',
            }
            Comment.objects.create(
                body=payload['body'],
                user=self.user,
            )


class TestImageModel(TestCase):
    """Test class for image"""

    def setUp(self):
        self.user = create_user()

    @patch('uuid.uuid4')
    def test_image_file_name_uuid(self, mock_uuid):
        """Test that image saved in the correct location."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = utils.upload_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/media/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)


class TestChatSessionModel(TestCase):
    """Test class of chat session model."""

    def setUp(self):
        self.user = create_user()

    def test_create_chat_session_success(self):
        """Test create a new chat session."""
        chat_session = ChatSession.objects.create(
            owner=self.user,
        )

        self.assertEqual(self.user.id, chat_session.owner.id)
        self.assertTrue(chat_session.id is not None)

    def test_create_chat_session_invalid_user(self):
        """Test create a new chat session with invalid user."""
        with self.assertRaises(Exception):
            ChatSession.objects.create()


class TestChatMessageModel(TestCase):
    """The test class of chat message."""

    def setUp(self):
        self.user = create_user()
        self.chat_session = ChatSession.objects.create(
            owner=self.user,
        )

    def test_create_chat_message_success(self):
        """Create a new chat message successful"""
        payload = {
            'body': 'Hello! This is first message.'
        }
        chat_message = ChatMessage.objects.create(
            user=self.user,
            chat_session=self.chat_session,
            body=payload['body']
        )

        self.assertEqual(chat_message.body, payload['body'])
        self.assertEqual(chat_message.user.id, self.user.id)
        self.assertEqual(chat_message.chat_session.id, self.chat_session.id)

    def test_create_chat_message_with_parent_success(self):
        """Create a new chat message with parent message successful"""
        payload = {
            'body': 'Hello! This is first message.'
        }
        chat_message = ChatMessage.objects.create(
            user=self.user,
            chat_session=self.chat_session,
            body=payload['body']
        )
        chat_message1 = ChatMessage.objects.create(
            user=self.user,
            chat_session=self.chat_session,
            body=payload['body'],
            parent=chat_message,
        )

        self.assertEqual(chat_message1.body, payload['body'])
        self.assertEqual(chat_message1.user.id, self.user.id)
        self.assertEqual(chat_message1.chat_session.id, self.chat_session.id)
        self.assertEqual(chat_message1.parent.id, chat_message.id)

    def test_create_chat_message_invalid_user(self):
        """Test create a new chat message with invalid user."""
        with self.assertRaises(Exception):
            payload = {
                'body': 'Hello! This is first message.'
            }
            ChatMessage.objects.create(
                chat_session=self.chat_session,
                body=payload['body']
            )

    def test_create_chat_message_invalid_chat_session(self):
        """Test create a new chat message with invalid chat session."""
        with self.assertRaises(Exception):
            payload = {
                'body': 'Hello! This is first message.'
            }
            ChatMessage.objects.create(
                user=self.user,
                body=payload['body']
            )


class TestChatMemberModel(TestCase):
    """The test class of chat member."""

    def setUp(self):
        self.user = create_user()
        self.chat_session = ChatSession.objects.create(
            owner=self.user,
        )

    def test_create_new_chat_member_success(self):
        """Test create a new chat member successful."""
        chat_member = ChatMember.objects.create(
            user=self.user,
            chat_session=self.chat_session,
        )

        self.assertEqual(chat_member.user.id, self.user.id)
        self.assertEqual(chat_member.chat_session.id, self.chat_session.id)

    def test_create_new_chat_member_invalid_user(self):
        """Test create a new chat member invalid user."""
        with self.assertRaises(Exception):
            ChatMember.objects.create(
                chat_session=self.chat_session,
            )

    def test_create_new_chat_member_invalid_chat_session(self):
        """Test create a new chat member invalid session."""
        with self.assertRaises(Exception):
            ChatMember.objects.create(
                user=self.user,
            )


class TestChatRoleModel(TestCase):
    """Test class of chat role model."""

    def setUp(self):
        self.user = create_user()
        self.chat_session = ChatSession.objects.create(
            owner=self.user,
        )

    def test_create_role_successful(self):
        """Test creating a new role successful."""
        role = ChatRole.objects.create(
            chat_session=self.chat_session,
            title='Core Member'
        )

        self.assertEqual(role.chat_session.id, self.chat_session.id)
        self.assertEqual(role.title, 'Core Member')

    def test_create_role_invalid_chat_session(self):
        """Test creating a new role with invalid chat session."""
        with self.assertRaises(Exception):
            ChatRole.objects.create(
                title='Core Member'
            )

    def test_create_role_invalid_title(self):
        """Test creating a new role with invalid title."""
        with self.assertRaises(Exception):
            ChatRole.objects.create(
                chat_session=self.chat_session,
                title=None,
            )
