"""
Views
"""
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser

from core.models import (
    UserImage,
    ExpiringLink
)

from . import serializers
from .permissions import ExpiringLinkAllowed


class CreateTokenView(ObtainAuthToken):
    """Create a token for user"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserImageListView(generics.ListAPIView):
    """List images"""
    serializer_class = serializers.UserImageListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict list to the authenticated user"""
        return UserImage.objects.filter(user=self.request.user).order_by('-when_created')


class UserImageCreateView(generics.CreateAPIView):
    """Create images"""
    queryset = UserImage.objects.all()
    serializer_class = serializers.UserImageCreateSerializer
    parser_classes = [MultiPartParser]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ExpiringLinkListView(generics.ListAPIView):
    """List expiring links"""
    serializer_class = serializers.ExpiringLinkListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ExpiringLinkAllowed]

    def get_queryset(self):
        """Restrict only to the registered user"""
        return ExpiringLink.objects.filter(image__user=self.request.user)


class ExpiringLinkCreateView(generics.CreateAPIView):
    """Create expiring link"""
    queryset = ExpiringLink.objects.all()
    serializer_class = serializers.ExpiringLinkCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ExpiringLinkAllowed]


class ExpiringLinkDetailView(generics.RetrieveAPIView):
    """Retrieve an instance"""
    queryset = ExpiringLink.objects.all()
    serializer_class = serializers.ExpiringLinkDetailSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        current_time = timezone.now()
        expiration_time = instance.created_on + timezone.timedelta(seconds=instance.expires_after)

        if current_time > expiration_time:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data)
