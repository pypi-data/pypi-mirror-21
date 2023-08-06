## -*- coding: utf-8 -*-
<%inherit file="/layout.mako"/>
<%page cached="True" />
<% 
category = data['instance']
related_items = data['related_items']
%>
<%def name="pagetitle()">
<%
category = data['instance']
%>
${category.name}
</%def>

<div class="ui-widget ui-rounded whitebg b1">

<h2 class="feature generic">${category.name}</h2>
##<p>${category.description}</p>

% if len(related_items) < 1:
<p class="messagebox pinkbg">There's no posts for this category at the
moment.</p>
% else:
<ul class="colorList greybg2">
% for entry in related_items:
% if entry.reviewed:
<li><a href="${entry.get_absolute_url()}">${entry.pub_date}, ${entry.title}</a></li>
% endif
% endfor
</ul>
% endif

<div class="ui-footer">
 <a href="/blog/categories/">View all categories.</a>
</div>

</div>
