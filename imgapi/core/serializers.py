"""
Serializers
"""
import uuid

from django.urls import reverse
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import (
    UserImage,
    ExpiringLink,
)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserImageListSerializer(serializers.ModelSerializer):
    """Serializer for listing images"""
    thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = [
            'name',
            'thumbnails',
        ]

    def get_thumbnails(self, instance):
        return instance.get_thumbnails()


class UserImageCreateSerializer(serializers.ModelSerializer):
    """Serializer for uploading images"""

    class Meta:
        model = UserImage
        fields = [
            'name',
            'image',
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return UserImage.objects.create(**validated_data)


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    """Serializer for listing expiring links"""

    class Meta:
        model = ExpiringLink
        fields = [
            'link'
        ]


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating an expiring link"""

    class Meta:
        model = ExpiringLink
        fields = [
            'image',
            'expires_after',
        ]

    def create(self, validated_data):
        link_id = uuid.uuid4()
        full_url = self.context['request'].build_absolute_uri(
            reverse('expiring-link-detail',
                    kwargs={'id': str(link_id)})
                    )
        expiring_link = ExpiringLink(id=link_id,
                                     image=self.validated_data['image'],
                                     expires_after=self.validated_data[
                                         'expires_after'
                                         ],
                                     link=full_url)
        expiring_link.save()

        return expiring_link


class ExpiringLinkDetailSerializer(serializers.ModelSerializer):
    """Serializer for Expiring link view"""

    class Meta:
        model = ExpiringLink
        fields = [
            'image'
        ]
