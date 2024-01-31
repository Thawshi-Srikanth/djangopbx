#
#    DjangoPBX
#
#    MIT License
#
#    Copyright (c) 2016 - 2022 Adrian Fretwell <adrian@djangopbx.com>
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#
#    Contributor(s):
#    Adrian Fretwell <adrian@djangopbx.com>
#

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from .models import (
    Domain, Profile, DefaultSetting, DomainSetting, ProfileSetting
)
from .serializers import (
    UserSerializer, GroupSerializer, DomainSerializer, ProfileSerializer, DefaultSettingSerializer,
    DomainSettingSerializer, ProfileSettingSerializer
)
from pbx.restpermissions import (
    AdminApiAccessPermission
)
from dialplans.dialplanfunctions import SwitchDp


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]


class DomainViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Domains to be viewed or edited.
    """
    queryset = Domain.objects.all().order_by('name')
    serializer_class = DomainSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.username)

    def perform_create(self, serializer):
        instance = serializer.save()
        SwitchDp().import_xml(instance.name, False, instance.id)  # Create dialplans
        DomainSetting.objects.create(
            domain_id=instance,   # Create default menu setting
            category='domain',
            subcategory='menu',
            value_type='text',
            value='Default',
            sequence=10,
            updated_by=self.request.user.username
            )


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows User Profiles to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by('username')
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['domain_id', 'username']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]


class DefaultSettingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Default Settings to be viewed or edited.
    """
    queryset = DefaultSetting.objects.all().order_by('category', 'subcategory')
    serializer_class = DefaultSettingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['app_uuid', 'category', 'subcategory', 'value_type']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]


class DomainSettingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Domain Settings to be viewed or edited.
    """
    queryset = DomainSetting.objects.all().order_by('domain_id', 'category', 'subcategory')
    serializer_class = DomainSettingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['domain_id', 'app_uuid', 'category', 'subcategory', 'value_type']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]


class ProfileSettingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Profile Settings to be viewed or edited.
    """
    queryset = ProfileSetting.objects.all().order_by('user_id', 'category', 'subcategory')
    serializer_class = ProfileSettingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'category', 'subcategory', 'value_type']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]
