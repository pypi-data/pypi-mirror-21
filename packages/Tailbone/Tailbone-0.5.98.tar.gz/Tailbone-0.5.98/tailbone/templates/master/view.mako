## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">${model_title}: ${instance_title}</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  % if master.has_rows:
      ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js'))}
      <script type="text/javascript">
        $(function() {
            $('.newgrid-wrapper').gridwrapper();
        });
      </script>
      <style type="text/css">
        .newgrid-wrapper {
            margin-top: 10px;
        }
      </style>
  % endif
</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to {}".format(model_title_plural), index_url)}</li>
  <li>${h.link_to("Permalink for this {}".format(model_title), action_url('view', instance))}</li>
  % if master.editable and instance_editable and request.has_perm('{}.edit'.format(permission_prefix)):
      <li>${h.link_to("Edit this {}".format(model_title), action_url('edit', instance))}</li>
  % endif
  % if master.deletable and instance_deletable and request.has_perm('{}.delete'.format(permission_prefix)):
      <li>${h.link_to("Delete this {}".format(model_title), action_url('delete', instance))}</li>
  % endif
  % if master.creatable and request.has_perm('{}.create'.format(permission_prefix)):
      <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
  % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->

% if master.has_rows:
    ${rows_grid|n}
% endif
