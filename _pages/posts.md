---
layout: default
title: Posts
permalink: /Posts/
---

<div class="posts">
	{% for post in paginator.posts %}
		{% if post.general != null %}
		{% else %}
			<div class="post">
				<h1 class="post-title">
					<a href="{{ post.url }}">
						{{ post.title }}
					</a>
				</h1>
				<span class="post-date">{{ post.date | date_to_string }}</span>
				{{ post.content }}
			</div>
		{% endif %}
	{% endfor %}
</div>