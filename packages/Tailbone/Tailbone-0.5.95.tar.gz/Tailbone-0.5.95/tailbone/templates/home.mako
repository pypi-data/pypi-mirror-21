## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Home</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    .logo {
        text-align: center;
    }
    .logo img {
        margin: 3em auto;
    }
  </style>
</%def>

<div class="logo">
  ${h.image(request.static_url('tailbone:static/img/home_logo.png'), "Rattail Logo")}
  <h1>Welcome to Tailbone</h1>
</div>
