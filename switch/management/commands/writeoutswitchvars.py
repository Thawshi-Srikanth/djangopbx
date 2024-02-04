#    DjangoPBX
#
#    MIT License
#
#    Copyright (c) 2016 - 2024 Adrian Fretwell <adrian@djangopbx.com>
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


import sys
from django.utils.translation import gettext_lazy as _
from django.core.management.base import BaseCommand
from switch.switchfunctions import SwitchFunctions


class Command(BaseCommand):
    help = 'Write Switch vars.xml'

    def handle(self, *args, **kwargs):
        r = SwitchFunctions().save_var_xml()
        if r == 0:
            print(_('vars.xml file written.'))
        if r == 1:
            print(_('Default setting does not exist:') + ' switch->conf')
        if r == 2:
            print(_('Configuration directory does not exist.'))
        if r == 3:
            print(_('Error writing to file.'))
