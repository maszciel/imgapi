import uuid

from PIL import Image

import os

from django.db import models
from django.conf import settings
from urllib.parse import urljoin
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a user"""
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and return a superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    BASIC = 'B'
    PREMIUM = 'P'
    ENTERPRISE = 'E'
    CUSTOM = 'C'

    USER_TIER_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
        (CUSTOM, 'Custom'),
    ]
    # Fields
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_tier = models.CharField(
        max_length=1,
        choices=USER_TIER_CHOICES,
        default=BASIC
    )
    custom_temp_link = models.BooleanField(default=False)
    custom_original_link = models.BooleanField(default=False)
    custom_thumbnail_size = models.IntegerField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

    @property
    def available_thumbnails(self):
        """
        Get available thumbnail heights.
        If True, a link to the original image is available.

        """
        if self.user_tier == self.BASIC:
            return [200]
        elif self.user_tier == self.PREMIUM:
            return [200, 400]
        elif self.user_tier == self.ENTERPRISE:
            return [200, 400, True]
        elif self.user_tier == self.CUSTOM:
            return [self.custom_thumbnail_size, self.custom_original_link]


class UserImage(models.Model):
    """Model for user-uploaded image"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to='media/',
        validators=[FileExtensionValidator(['png', 'jpg'])],
        max_length=255
        )
    name = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    when_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url

    def get_original_img_url(self):
        return self.image.url

    def get_desired_width(self, curr_width, curr_height, height):
        """
        Get width that will allow to retain
        the appropriate ratio after resize
        """
        return int((curr_width * height) / curr_height)

    def get_thumbnails(self):
        """Get thumbnail urls"""

        thumbnails = []
        img_path = self.image.path

        for height in self.user.available_thumbnails:
            if type(height) is int:
                with Image.open(img_path) as img:
                    img_copy = img.copy()
                    w, h = img_copy.size
                    width = self.get_desired_width(w, h, height)
                    # Resize
                    img_copy.thumbnail((width, height))

                    img_dir = os.path.dirname(img_path)
                    thumbnail_name = f'{str(height)}_{os.path.basename(img_path)}'
                    thumbnail_path = os.path.join(img_dir,
                                                  'thumbnails',
                                                  thumbnail_name)

                    img_copy.save(thumbnail_path)

                    # Will be a URL in production
                    thumbnail_url = urljoin(settings.MEDIA_URL, thumbnail_path)

                    thumbnails.append(thumbnail_url)
            elif type(height) is bool and height:
                thumbnails.append(self.get_original_img_url)

        return thumbnails


class ExpiringLink(models.Model):
    """Model for expiring links"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(UserImage, on_delete=models.CASCADE)
    expires_after = models.IntegerField(default=350,
                                        validators=[
                                            MinValueValidator(300),
                                            MaxValueValidator(30000)
                                            ])
    link = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        pass
