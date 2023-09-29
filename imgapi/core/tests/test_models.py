"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import (
    User,
    UserImage,
    ExpiringLink,
)


def create_user(email='test@example.com',
                password='test1234',
                user_tier=User.BASIC,
                **extra_fields,):
    """Create and return user"""
    return get_user_model().objects.create_user(email=email,
                                                password=password,
                                                user_tier=user_tier,
                                                **extra_fields)


class ModelTests(TestCase):
    """Test models"""

    def test_user_created(self):
        """Test user created successfully"""
        user = create_user()

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.user_tier, User.BASIC)
        self.assertTrue(user.check_password('test1234'))

    def test_user_email_required(self):
        """"Test if empty email field raises Value Error"""
        with self.assertRaises(ValueError):
            create_user(email="")

    def test_superuser_created(self):
        superuser = get_user_model().objects.create_superuser(
            email="test@example.com",
            password="test12345",
        )

        self.assertEqual(superuser.email, 'test@example.com')
        self.assertEqual(superuser.user_tier, User.BASIC)
        self.assertTrue(superuser.check_password('test12345'))

    def test_available_thumbnail_property(self):
        user1 = create_user()
        user2 = create_user(email='test2@example.com',
                            user_tier=User.PREMIUM)
        user3 = create_user(email='test3@example.com',
                            user_tier=User.ENTERPRISE)
        user4 = create_user(email='test4@example.com',
                            user_tier=User.CUSTOM,
                            custom_thumbnail_size=500)

        self.assertEqual(user1.available_thumbnails, [200])
        self.assertEqual(user2.available_thumbnails, [200, 400])
        self.assertEqual(user3.available_thumbnails, [200, 400, True])
        self.assertEqual(user4.available_thumbnails, [500, False])

    def test_image_created(self):
        """Test image created successfuly"""
        user = create_user()
        img = UserImage.objects.create(image="media/media/test/test.png",
                                       user=user)

        self.assertEqual(img.user, user)

    def test_expiring_link_created(self):
        user = create_user(user_tier=User.ENTERPRISE)
        image = UserImage.objects.create(image="media/media/test/test.png",
                                         user=user)
        exp_link = ExpiringLink.objects.create(image=image,
                                               expires_after=300)

        self.assertEqual(exp_link.image.id, image.id)
