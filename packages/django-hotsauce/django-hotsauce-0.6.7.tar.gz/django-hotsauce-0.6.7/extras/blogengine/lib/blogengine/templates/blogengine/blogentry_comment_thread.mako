## -*- coding: utf-8 -*-
<%def name="comments_for_item()">
<%
result = data['result'] 
media_prefix = data['MEDIA_URL']
comments = data['comments']
comment_count = len(comments)
u_comment_count = data['u_comments_count']
comments.sort(lambda x, y: cmp(x.pub_date, y.pub_date))
##settings = data['request'].session.settings
##comments.reverse()
%>

<div id="commentPanel" class="ui-comment-thread">
<h2 class="feature generic">Recent Comments (${comment_count})</h2>
% if comments:
##(${u_comment_count} comment waiting in line)
% for comment in comments:
<% comment_id = comment.s.oid %>
<div class="ui-comment-hd" id="#comment${comment_id}">
<a href="#comment${comment_id}">${comment.sender_name} posted a reply on ${comment.pub_date.strftime("%Y-%m-%d")}</a>
</div>
<div class="ui-comment">
##<a href="#" title="View comment">View comment</a>
<div class="ui-comment-bd">
 ${comment.convert_to_html()}
## <%include file="blogentry_comment_footer.mako" />
</div>
</div>
% endfor
<br/>
% else:
No comments yet!
% endif
</div>

<%include file="blogentry_comment_form.mako" />

</%def>
##${headline(result, nolinks=True)}
