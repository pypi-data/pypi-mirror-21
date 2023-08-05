# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2016 Lance Edgar
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
Common stuff for tempmon views
"""

from __future__ import unicode_literals, absolute_import

from formalchemy.fields import SelectFieldRenderer
from webhelpers.html import tags

from tailbone import views
from tailbone.db import TempmonSession


class MasterView(views.MasterView):
    """
    Base class for tempmon views.
    """
    Session = TempmonSession


class ClientFieldRenderer(SelectFieldRenderer):

    def render_readonly(self, **kwargs):
        client = self.raw_value
        if not client:
            return ''
        return tags.link_to(client, self.request.route_url('tempmon.clients.view', uuid=client.uuid))


class ProbeFieldRenderer(SelectFieldRenderer):

    def render_readonly(self, **kwargs):
        probe = self.raw_value
        if not probe:
            return ''
        return tags.link_to(probe, self.request.route_url('tempmon.probes.view', uuid=probe.uuid))
