## -*- coding: utf-8 -*-
<%namespace name="base" file="tailbone:templates/base.mako" />            
<%namespace file="/menu.mako" import="main_menu_items" />
<%namespace file="/newgrids/nav.mako" import="grid_index_nav" />
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${self.global_title()} &raquo; ${capture(self.title)|n}</title>
    ${self.favicon()}
    ${self.header_core()}

    % if not request.rattail_config.production():
        <style type="text/css">
          body { background-image: url(${request.static_url('tailbone:static/img/testing.png')}); }
        </style>
    % endif

    ${self.head_tags()}
  </head>

  <body>
    <div id="body-wrapper">

      <header>
        <nav>
          <ul class="menubar">
            ${main_menu_items()}
          </ul>
        </nav>

        <div class="global">
          <a class="home" href="${url('home')}">
            ${self.header_logo()}
            <span class="title">${self.global_title()}</span>
          </a>
          % if master:
              <span class="global">&raquo;</span>
              % if master.listing:
                  <span class="global">${model_title_plural}</span>
              % else:
                  ${h.link_to(index_title, index_url, class_='global')}
                  % if master.viewing and grid_index:
                      ${grid_index_nav()}
                  % endif
              % endif
          % endif

          <div class="feedback">
            ${h.link_to("Feedback", url('feedback'), class_='button')}
          </div>

        </div><!-- global -->

        <div class="page">
          ${self.content_title()}
        </div>
      </header>

      <div class="content-wrapper">
        
        <div id="scrollpane">
          <div id="content">
            <div class="inner-content">

              % if request.session.peek_flash('error'):
                  <div class="error-messages">
                    % for error in request.session.pop_flash('error'):
                        <div class="ui-state-error ui-corner-all">
                          <span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-alert"></span>
                          ${error}
                        </div>
                    % endfor
                  </div>
              % endif

              % if request.session.peek_flash():
                  <div class="flash-messages">
                    % for msg in request.session.pop_flash():
                        <div class="ui-state-highlight ui-corner-all">
                          <span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-info"></span>
                          ${msg|n}
                        </div>
                    % endfor
                  </div>
              % endif

              ${self.body()}

            </div><!-- inner-content -->
          </div><!-- content -->
        </div><!-- scrollpane -->

      </div><!-- content-wrapper -->

      <div id="footer">
        ${self.footer()}
      </div>

    </div><!-- body-wrapper -->

  </body>
</html>

<%def name="app_title()">Rattail</%def>

<%def name="global_title()">${"[STAGE] " if not request.rattail_config.production() else ''}${self.app_title()}</%def>

<%def name="content_title()">
  <h1>${self.title()}</h1>
</%def>

<%def name="favicon()"></%def>

<%def name="header_core()">
  ${base.core_javascript()}
  ${self.extra_javascript()}
  ${base.core_styles(jquery_theme=self.jquery_theme)}
  ${self.extra_styles()}
</%def>

<%def name="jquery_theme()">
    ${h.stylesheet_link('https://code.jquery.com/ui/1.11.4/themes/dark-hive/jquery-ui.css')}
</%def>

<%def name="extra_javascript()"></%def>

<%def name="extra_styles()">
    ${h.stylesheet_link(request.static_url('tailbone:static/css/theme-better.css'))}
</%def>

<%def name="head_tags()"></%def>

<%def name="header_logo()"></%def>

<%def name="footer()">
   powered by ${h.link_to("Rattail", url('about'))}
</%def>

<%def name="wtfield(form, name, **kwargs)">
  <div class="field-wrapper${' error' if form[name].errors else ''}">
    <label for="${name}">${form[name].label}</label>
    <div class="field">
      ${form[name](**kwargs)}
    </div>
  </div>
</%def>
