## -*- coding: utf-8 -*-
<%inherit file="/layout.mako" />

<%page cached="False" />
<%namespace file="components.mako" import="headline, pager" />

<%
## Get the latest entries and sort them by their
## pub_date in descending order.
entries = data['blogentry_set']
##entries.sort(lambda x, y: cmp(x.pub_date, y.pub_date))
##entries.reverse()
entries_count = data['max_items_count']
categories = data['blog_categories']
page_num = data['page_num']
page_mod = data['page_mod']
next_page = data['next_page']
prev_page = data['prev_page']
##settings = data['settings']
##request = data['request']
%>

<%def name="pagetitle()">
Blog
</%def>

## synbio = biological exploits (scientist = moo eVi| h4ck3rz)
<%def name="latest_posts(entries, title='Nouvelles')" cached="True">
<div class="fl ui-widget whitebg ui-rounded ui-generic b1 col300">
<h2 class="feature generic">${title}</h2>
<ul class="colorList greybg2">
%for item in entries:
<li>
<a href="${item.get_absolute_url()}" title="${item}">${item}</a>
</li>
%endfor
</ul>
##${pager()}
## front-end admin panel
##% if request.user:
##<div class="ui-button generic bluebg">
## <span><a href="/blog/posts/add/">Create a new article</a></span>
##</div>
##% endif
</div>
</%def>

${latest_posts(entries)}

<div class="fl ui-widget col300 whitebg ui-rounded ui-generic b1">
<h2 class="feature generic">Categories</h2>
<ul class="colorList greybg">
% for item in categories:
<li><a href="/blog/categories/${item.slug}/">${item.slug} (${item.get_items_count()})</a></li>
% endfor
</ul>

##<div class="generic greybg2">
##<h2 class="message pinkbg">Bookmarks</h2>
##<ul id="rss-widget" class="colorList">
##</ul>
##% if 'DELICIOUS_USERNAME' in settings:
##<%include file="delicious_widget.mako" />
##% endif
##</div>
</div>
<br class="clear"/>

<%def name="extra_js()">
<% media_prefix = data['MEDIA_URL'] %>
<script src="${media_prefix}js/jquery/jquery-1.7.2.min.js"></script>
<script src="${media_prefix}js/tm_api-2.0/src/colorlist.min.js"> </script>
<script src="${media_prefix}js/setup.js"></script>
##<% prefix = data['MEDIA_URL'] %>
##<script src="${prefix}js/tm_api-2.0/src/colorlist.js" type="text/javascript"></script>
##<script>
##(function($){
## custom accordion navigation (left)
##$('#col1').accordion({
##header: 'h3',
##active: false,
##event: 'mouseover'
##});
##$('#rss-widget').getFeed('/feeds/21/', 'li');
##$('ul.colorList').eq(0).colorList({class: 'pinkbg'});
##})(jQuery);
##</script>
</%def>

##${extra_js()}
