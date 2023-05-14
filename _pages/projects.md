---
layout: default
title: Projects
category: _projects
permalink: /Projects/
---
<div class="posts">
	{% for post in paginator.posts %}
		{% if post._pages == null %}
			<div class="post">
				<h1 class="post-title">
					<a href="{{ post.url }}">
						{{ post.title }}
					</a>
				</h1>
				<span class="post-date">{{ post.date | date_to_string }}</span>
				{{ post.content }}
			</div>
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