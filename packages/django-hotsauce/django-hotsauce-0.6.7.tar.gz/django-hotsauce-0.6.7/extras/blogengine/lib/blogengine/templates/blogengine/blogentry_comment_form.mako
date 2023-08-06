## coding: utf-8
<% 
##media_prefix = data['MEDIA_URL'] 
##settings = data['request'].session.settings
result = data['result']
comment_form = data['comment_form']
%>

<%page cached="True"/>

<div id="commentform" class="greybg generic b1">
<span class="ui-slide-down">Add comment</span>
##<span class="ui-slide-up">Close</span>
<form action="/comment/new/" method="post">
<table> 
${comment_form.as_table()}
</table>
<input type="hidden" name="id_path" value="${result.get_absolute_url()}"/>
<input type="hidden" name="id_oid" value="${result.s.oid}"/>

<input type="submit" />
</form>
</div>

##${self.extra_css(media_prefix)}
