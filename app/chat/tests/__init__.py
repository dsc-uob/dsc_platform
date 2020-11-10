from django.urls import reverse
from django.contrib.auth import get_user_model

LIST_CHAT_SESSION_URL = reverse('chat:session')
CREATE_CHAT_SESSION_URL = reverse('chat:create')


def MANAGE_CHAT_SESSION_URL(args):
    return reverse('chat:session', args=args)


def create_user(email='user@test.com', username='testuser',
                first_name='test', password='1234abcd'):
    return get_user_model().objects. \
        create_user(email=email, username=username,
                    first_name=first_name, password=password)
