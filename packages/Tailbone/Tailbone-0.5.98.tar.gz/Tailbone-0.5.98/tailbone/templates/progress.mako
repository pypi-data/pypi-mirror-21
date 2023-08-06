## -*- coding: utf-8 -*-
<%namespace file="tailbone:templates/base.mako" import="core_javascript" />
<%namespace file="/base.mako" import="jquery_theme" />
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html style="direction: ltr;" xmlns="http://www.w3.org/1999/xhtml" lang="en-us">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>Working...</title>
    ${core_javascript()}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/normalize.css'))}
    ${jquery_theme()}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/base.css'))}
    ${h.stylesheet_link(request.static_url('tailbone:static/css/layout.css'))}
    <style type="text/css">

      #body-wrapper {
          position: relative;
      }

      #wrapper {
          height: 60px;
          left: 50%;
          margin-top: -45px;
          margin-left: -350px;
          position: absolute;
          top: 50%;
          width: 700px;
      }

      #progress-wrapper {
          border-collapse: collapse;
      }

      #progress {
          border-collapse: collapse;
          height: 25px;
          width: 550px;
      }

      #complete {
          background-color: Gray;
          width: 0px;
      }

      #remaining {
          background-color: LightGray;
          width: 100%;
      }

      #percentage {
          padding-left: 3px;
          min-width: 50px;
          width: 50px;
      }

      #cancel .ui-button-text {
          white-space: nowrap;
      }

    </style>
    <script language="javascript" type="text/javascript">

      var updater = null;

      function update_progress() {
          $.ajax({
              url: '${url('progress', key=key)}',
              success: function(data) {
                  if (data.error) {
                      location.href = '${cancel_url}';
                  } else if (data.complete || data.maximum) {
                      $('#message').html(data.message);
                      $('#total').html('('+data.maximum_display+' total)');
                      $('#cancel button').show();
                      if (data.complete) {
                          clearInterval(updater);
                          $('#cancel button').hide();
                          $('#total').html('done!');
                          $('#complete').css('width', '100%');
                          $('#remaining').hide();
                          $('#percentage').html('100 %');
                          location.href = data.success_url;
                      } else {
                          var width = parseInt(data.value) / parseInt(data.maximum);
                          width = Math.round(100 * width);
                          if (width) {
                              $('#complete').css('width', width+'%');
                              $('#percentage').html(width+' %');
                          } else {
                              $('#complete').css('width', '0.01%');
                              $('#percentage').html('0 %');
                          }
                          $('#remaining').css('width', 'auto');
                      }
                  }
              },
          });
      }

      updater = setInterval(function() {update_progress()}, 1000);

      $(function() {

          $('#cancel button').click(function() {
              if (confirm("Do you really wish to cancel this operation?")) {
                  clearInterval(updater);
                  $(this).button('disable').button('option', 'label', "Canceling, please wait...");
                  $.ajax({
                      url: '${url('progress.cancel', key=key)}',
                      data: {
                          'cancel_msg': '${cancel_msg}',
                      },
                      success: function(data) {
                          location.href = '${cancel_url}';
                      },
                  });
              }
          });

      });

      </script>
  </head>
  <body>
    <div id="body-wrapper">

      <div id="wrapper">

        <p><span id="message">${initial_msg or "Working"} (please wait)</span> ... <span id="total"></span></p>

        <table id="progress-wrapper">
          <tr>
            <td>
              <table id="progress">
                <tr>
                  <td id="complete"></td>
                  <td id="remaining"></td>
                </tr>
              </table><!-- #progress -->
            </td>
            <td id="percentage"></td>
            <td id="cancel">
              <button type="button" style="display: none;">Cancel</button>
            </td>
          </tr>
        </table><!-- #progress-wrapper -->

      </div><!-- #wrapper -->

    </div><!-- #body-wrapper -->
  </body>
</html>
