from django.urls import reverse
from django.contrib.auth import get_user_model

POSTS_URL = reverse('post_sys:post-list')
COMMENT_URL = reverse('post_sys:comment-list')


def create_user(email='user@test.com', username='testuser',
                first_name='test', password='1234abcd'):
    return get_user_model().objects. \
        create_user(email=email, username=username,
                    first_name=first_name, password=password)
