## -*- coding: utf-8 -*-
<%inherit file="/master/edit.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js'))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.batch.js'))}
  <script type="text/javascript">

    var has_execution_options = ${'true' if master.has_execution_options else 'false'};

    $(function() {

        $('#save-refresh').click(function() {
            var form = $(this).parents('form');
            form.append($('<input type="hidden" name="refresh" value="true" />'));
            form.submit();
        });

    });
  </script>
  <style type="text/css">

    .newgrid-wrapper {
        margin-top: 10px;
    }
    
  </style>
</%def>

<%def name="buttons()">
    <div class="buttons">
      % if master.refreshable:
          ${h.submit('save-refresh', "Save & Refresh Data")}
      % endif
      % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
          <button type="button" id="execute-batch"${'' if execute_enabled else ' disabled="disabled"'}>${execute_title}</button>
      % endif
    </div>
</%def>

<%def name="grid_tools()">
    % if not batch.executed:
        <p>${h.link_to("Delete all rows matching current search", url('{}.delete_rows'.format(route_prefix), uuid=batch.uuid))}</p>
    % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
## TODO: clean this up or fix etc..?
##   % if master.edit_with_rows:
##       ${form.render(buttons=capture(buttons))|n}
##   % else:
      ${form.render()|n}
##   % endif
</div>

% if master.edit_with_rows:
    ${rows_grid.render_complete(allow_save_defaults=False, tools=capture(self.grid_tools))|n}
% endif

<div id="execution-options-dialog" style="display: none;">

  ${h.form(url('{}.execute'.format(route_prefix), uuid=batch.uuid), name='batch-execution')}
  % if master.has_execution_options:
      ${rendered_execution_options|n}
  % endif
  ${h.end_form()}

</div>
