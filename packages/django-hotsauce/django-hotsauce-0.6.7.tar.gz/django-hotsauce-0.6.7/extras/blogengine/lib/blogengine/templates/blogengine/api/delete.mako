## coding: utf-8 
<%inherit file="/layout.mako" />
<%
request = data['request']
user = request.remote_user
message = data['message'] or ''
instance = data['instance']
deleted = data['deleted']
%>

<%def name="pagetitle()">
Delete post
</%def>


<div class="ui-editor whitebg ui-generic ui-rounded" id="ui-editor-0">
<h2 class="feature generic">Delete post</h2>
% if message != '':
${message}
% endif
% if not deleted:
<legend>Entry: ${instance}</legend>
<form id="deleteEntryForm" action="." method="POST" enctype="multipart/form-data">
 Delete this object?
 <input type="submit" value="Yes">
</form>
% endif

##% if form.errors:
##<div class="messagebox error">
##${form.errors}
##</div>
##% endif


</div>
