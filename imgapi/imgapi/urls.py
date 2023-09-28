"""imgapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import settings

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/',
         SpectacularAPIView.as_view(),
         name='api-schema'),
    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('image/',
         views.UserImageListView.as_view(),
         name='image-list'),
    path('image/create',
         views.UserImageCreateView.as_view(),
         name='image-create'),
    path('expiring-link/',
         views.ExpiringLinkListView.as_view(),
         name='expiring-link-list'),
    path('expiring-link/create',
         views.ExpiringLinkCreateView.as_view(),
         name='expiring-link-create'),
    path('expiring-link/<uuid:id>',
         views.ExpiringLinkDetailView.as_view(),
         name='expiring-link-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
