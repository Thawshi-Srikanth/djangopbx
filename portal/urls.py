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

from django.urls import path, re_path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'menus', views.MenuViewSet)
router.register(r'menu_items', views.MenuItemViewSet)
router.register(r'menu_item_groups', views.MenuItemGroupViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('domainselect/', views.DomainSelector.as_view(), name='domainselect'),
    path('selectdomain/<domainuuid>/', views.selectdomain, name='selectdomain'),
    path(
        'favicon.ico',
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    re_path(
        r'^(?P<fullpath>(?P<fs>fs)/(?P<fdir>.*)/(?P<fdom>.*)/(?P<fpath>.*))$',
        views.servefsmedia, name='servefsmedia'
        ),
    re_path(r'clickdial/(?P<dest>[A-Za-z0-9\.@]+)/', views.ClickDial.as_view(), name='clickdial'),
    path('pbxlogout/', views.pbxlogout, name='pbxlogout'),
]
