## -*- coding: utf-8 -*-
## ##############################################################################
## 
## Default master 'index' template.  Features a prominent data table and
## exposes a way to filter and sort the data, etc.  Some index pages also
## include a "tools" section, just above the grid on the right.
## 
## ##############################################################################
<%inherit file="/base.mako" />

<%def name="title()">${grid.model_title_plural}</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js'))}
  <script type="text/javascript">
    $(function() {

        $('.newgrid-wrapper').gridwrapper();

        % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):

            $('form[name="merge-things"] button').button('option', 'disabled', $('.newgrid tbody td.checkbox input:checked').length != 2);

            $('.newgrid-wrapper').on('click', 'tbody td.checkbox input', function() {
                $('form[name="merge-things"] button').button('option', 'disabled', $('.newgrid tbody td.checkbox input:checked').length != 2);
            });


            $('form[name="merge-things"]').submit(function() {
                var uuids = [];
                $('.newgrid tbody td.checkbox input:checked').each(function() {
                    uuids.push($(this).parents('tr:first').data('uuid'));
                });
                if (uuids.length != 2) {
                    return false;
                }
                $(this).find('[name="uuids"]').val(uuids.toString());
                $(this).find('button')
                    .button('option', 'label', "Preparing to Merge...")
                    .button('disable');
            });

        % endif

        % if master.bulk_deletable and request.has_perm('{}.bulk_delete'.format(permission_prefix)):

        $('form[name="bulk-delete"] button').click(function() {
            var count = 0;
            var match = /showing \d+ thru \d+ of (\S+)/.exec($('.pager .showing').text());
            if (match) {
                count = match[1];
            } else {
                alert("There don't seem to be any results to delete!");
                return;
            }
            if (! confirm("You are about to delete " + count + " ${model_title_plural}.\n\nAre you sure?")) {
                return
            }
            $(this).button('disable').button('option', 'label', "Deleting Results...");
            $('form[name="bulk-delete"]').submit();
        });

        % endif
    });
  </script>
</%def>

<%def name="context_menu_items()">
  % if master.creatable and request.has_perm('{}.create'.format(grid.permission_prefix)):
      <li>${h.link_to("Create a new {}".format(grid.model_title), url('{}.create'.format(grid.route_prefix)))}</li>
  % endif
</%def>

<%def name="grid_tools()">
  % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):
      ${h.form(url('{}.merge'.format(route_prefix)), name='merge-things')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="submit">Merge 2 ${model_title_plural}</button>
      ${h.end_form()}
  % endif
  % if master.bulk_deletable and request.has_perm('{}.bulk_delete'.format(permission_prefix)):
      ${h.form(url('{}.bulk_delete'.format(route_prefix)), name='bulk-delete')}
      ${h.csrf_token(request)}
      <button type="button">Delete Results</button>
      ${h.end_form()}
  % endif
</%def>

${grid.render_complete(tools=capture(self.grid_tools).strip(), context_menu=capture(self.context_menu_items).strip())|n}
