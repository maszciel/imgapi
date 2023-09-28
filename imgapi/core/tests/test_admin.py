"""
Tests for custom admin page
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for the admin page"""
    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass1234',
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user5@example.com',
            password='testpass124',
            name='Test',
        )

    def test_list_user(self):
        """Test listing users"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test__user_page(self):
        """Test editing users"""
        url = reverse('admin:core_user_changelist', )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    def test_create_user(self):
        """Test creating a user"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)