---
layout: default
title: Posts
category: _posts
permalink: /Posts/
---
{% raw %}
{% for post in site.posts %}
  {% if post.categories contains 'blog1' %}
	<div class="post">
		<h3 class="title"><a href="{{ post.url }}">{{ post.title }}</a></h3>
		<p class="meta">Date: {{ post.date }}</p>
		<div class="entry">
			{{ post.content | strip_html | truncatewords: 100 }}
		</div>
	</div>
  {% endif %}
{% endfor %}
{% endraw %}