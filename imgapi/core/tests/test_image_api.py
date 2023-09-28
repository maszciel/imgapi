import tempfile
import os
import shutil

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import User, UserImage, ExpiringLink
from core import serializers

IMG_URL = reverse('image-list')
IMG_CREATE_URL = reverse('image-create')
TEMP_LINK_URL = reverse('expiring-link-list')
TEMP_LINK_CREATE_URL = reverse('expiring-link-create')
TEST_DIR = 'test_image'


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserImageAPITest(TestCase):
    """Test User Image API"""

    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """Test if listing images requires authentication"""
        res = self.client.get(IMG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserImageAPITest(TestCase):
    """Tests for authenticated requests to the API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(user=self.user)

    @override_settings(MEDIA_ROOT=os.path.join(TEST_DIR, 'media'))
    def test_create_user_image(self):
        """Test creating image"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:

            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(IMG_CREATE_URL, payload, format='multipart')
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)

    @override_settings(MEDIA_ROOT=os.path.join(TEST_DIR, 'test'))
    def test_list_user_images(self):
        """Test user can list their images"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            self.client.post(IMG_CREATE_URL, payload, format='multipart')

        res = self.client.get(IMG_URL)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_exp_link_list_and_create(self):
        """Test listing and creating expiring links"""
        user2 = create_user(email='email@example.com', password='Testpass12345', user_tier=User.ENTERPRISE)
        self.client.force_authenticate(user=user2)
        img = UserImage.objects.create(image="media/media/test/test.png",
                                       user=user2)
        payload = {
            'image': img.id,
            'expires_after': 300,
        }

        res = self.client.post(TEMP_LINK_CREATE_URL, payload)
        res2 = self.client.get(TEMP_LINK_URL)
        links = ExpiringLink.objects.all()
        serializer1 = serializers.ExpiringLinkListSerializer(links)
        serializer2 = serializers.ExpiringLinkListSerializer(res2)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res2.data), 1)
        self.assertEqual(serializer2.data, serializer1.data)
        
        self.client.force_authenticate(self.user)        

    def test_basic_users_not_allowed_expiring_link(self):
        """Test if basic users are not allowed to list or create expiring link"""
        img = UserImage.objects.create(image="media/media/test/test.png",
                                       user=self.user)
        payload = {
            'image': img.id,
            'expires_after': 300,
        }

        res = self.client.post(TEMP_LINK_CREATE_URL, payload)
        res2 = self.client.get(TEMP_LINK_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
        os.makedirs('/app/test_image/test/media/thumbnails')