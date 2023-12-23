#
#    DjangoPBX
#
#    MIT License
#
#    Copyright (c) 2016 - 2023 Adrian Fretwell <adrian@djangopbx.com>
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

from django.views import View
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import LoginRequiredMixin


from pbx.restpermissions import (
    AdminApiAccessPermission
)
from .models import (
    AutoReports, AutoReportSections,
)
from .serializers import (
    AutoReportsSerializer, AutoReportSectionsSerializer,
)
from .autoreportfunctions import ArFunctions


class AutoReportsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AutoReports to be viewed or edited.
    """
    queryset = AutoReports.objects.all().order_by('domain_id', 'name')
    serializer_class = AutoReportsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['domain_id', 'name']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]


class AutoReportSectionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AutoReportSections to be viewed or edited.
    """
    queryset = AutoReportSections.objects.all().order_by('auto_report_id', 'sequence')
    serializer_class = AutoReportSectionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['auto_report_id', 'sequence']
    permission_classes = [
        permissions.IsAuthenticated,
        AdminApiAccessPermission,
    ]


class ViewReport(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        r = kwargs.get('report', '')
        arf = ArFunctions(None, r)
        return render(request, 'autoreports/viewreport.html', {'d': arf.gen_report()})
