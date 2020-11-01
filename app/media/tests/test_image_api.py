import tempfile

from PIL import Image

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core import models

IMAGE_URL = reverse('media:image-list')


def create_user(email='user@test.com', username='testuser',
                first_name='test', password='1234abcd'):
    return get_user_model().objects. \
        create_user(email=email, username=username,
                    first_name=first_name, password=password)


class PublicImageApiTest(TestCase):
    """Test the public api of images"""

    def setUp(self):
        self.client = APIClient()

    def test_no_images_unauthorized(self):
        """Test retrieve no image for unauthorized calls."""
        res = self.client.get(IMAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_create_image_unauthorized(self):
        """Test can't create a new image in unauthorized calls."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(IMAGE_URL, data={'image': ntf},
                                   format='multipart')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateImageApiTest(TestCase):
    """The test class of image"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()

        self.client.force_authenticate(self.user)

    def tearDown(self):
        images = models.Image.objects.all()

        for img in images:
            img.image.delete()

    def test_created_image_successful(self):
        """Test create and return image successful."""
        with tempfile.NamedTemporaryFile(suffix='.png') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='PNG')
            ntf.seek(0)
            res = self.client.post(IMAGE_URL, data={'image': ntf},
                                   format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)

    def test_created_invalid_image(self):
        """Test create invalid image."""
        res = self.client.post(IMAGE_URL,
                               data={'image': 'no_image'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
