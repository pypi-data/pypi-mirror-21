# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2017 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Base View Class
"""

from __future__ import unicode_literals, absolute_import

import os

from rattail.db import model

from pyramid import httpexceptions
from pyramid.renderers import render_to_response
from pyramid.response import FileResponse

from tailbone.db import Session
from tailbone.auth import logout_user


class View(object):
    """
    Base class for all class-based views.
    """

    def __init__(self, request):
        self.request = request

        # if user becomes inactive while logged in, log them out
        if getattr(request, 'user', None) and not request.user.active:
            headers = logout_user(request)
            raise self.redirect(request.route_url('home'))

        config = self.rattail_config
        if config:
            self.enum = config.get_enum()

    @property
    def rattail_config(self):
        """
        Reference to the effective Rattail config object.
        """
        return getattr(self.request, 'rattail_config', None)

    def notfound(self):
        return httpexceptions.HTTPNotFound()
    
    def late_login_user(self):
        """
        Returns the :class:`rattail:rattail.db.model.User` instance
        corresponding to the "late login" form data (if any), or ``None``.
        """
        if self.request.method == 'POST':
            uuid = self.request.POST.get('late-login-user')
            if uuid:
                return Session.query(model.User).get(uuid)

    def redirect(self, url, **kwargs):
        """
        Convenience method to return a HTTP 302 response.
        """
        return httpexceptions.HTTPFound(location=url, **kwargs)

    def render_progress(self, kwargs):
        """
        Render the progress page, with given kwargs as context.
        """
        return render_to_response('/progress.mako', kwargs, request=self.request)

    def file_response(self, path):
        """
        Returns a generic FileResponse from the given path
        """
        if not os.path.exists(path):
            return self.notfound()
        response = FileResponse(path, request=self.request)
        response.headers[b'Content-Length'] = str(os.path.getsize(path))
        filename = os.path.basename(path).encode('ascii', 'replace')
        response.headers[b'Content-Disposition'] = b'attachment; filename="{}"'.format(filename)
        return response


def fake_error(request):
    """
    View which raises a fake error, to test exception handling.
    """
    raise Exception("Fake error, to test exception handling.")


def includeme(config):
    config.add_route('fake_error', '/fake-error')
    config.add_view(fake_error, route_name='fake_error',
                    permission='admin')
