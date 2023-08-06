## -*- encoding: utf-8 -*-
<%inherit file="/layout.mako" />
<%page cached="False" />
<%
request = data['request']
user = request.get_remote_user()
form = data['form']
message = data['message']
title = data['title'].encode('utf-8', 'replace')
oid = data['oid']
%>

<%def name="pagetitle()">
Edit post
</%def>



<%def name="extra_js()">
<%
media_prefix = data['MEDIA_URL']
%>
<script type="text/javascript" src="${media_prefix}js/jquery/jquery.autocomplete.min.js">
</script>
</%def>



<div class="ui-editor whitebg ui-generic ui-rounded" id="ui-editor-0">

<h2 class="feature generic">Blog admin: "${title}"</h2>

<form id="editEntryForm" action="." method="POST"> 
<table>
 <tbody>
 ${form.as_table()}
 </tbody>
</table>
 <div class="messagebox pinkbg ar">
  <input id="saveBtn" type="submit" value="Save changes" />
 </div>

</form>
${message}
</div>

${extra_js()}
