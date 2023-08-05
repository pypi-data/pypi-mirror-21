## -*- coding: utf-8 -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">Home</%def>

<%def name="page_title()"></%def>

<div style="text-align: center;">
  ${h.image(request.static_url('tailbone:static/img/home_logo.png'), "Rattail Logo", width='400')}
  <h1>Welcome to Tailbone</h1>
</div>
