## -*- coding: utf-8 -*-
<%inherit file="tailbone:templates/master/edit.mako" />

<%def name="title()">Edit: ${instance_title}</%def>

<%def name="context_menu_items()">
  % if master.viewable and request.has_perm('{}.view'.format(permission_prefix)):
      <li>${h.link_to("View this {}".format(model_title), action_url('view', instance))}</li>
  % endif
  % if master.deletable and instance_deletable and request.has_perm('{}.delete'.format(permission_prefix)):
      <li>${h.link_to("Delete this {}".format(model_title), action_url('delete', instance))}</li>
  % endif
  % if master.creatable and request.has_perm('{}.create'.format(permission_prefix)):
      <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
  % endif
</%def>

${parent.body()}
