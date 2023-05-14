---
layout:    default
title:     "Posts"
permalink: /Posts/
---

{% for project in site.posts %}
  <article>
    <h2><a href="{{ project.url }}">{{ project.title }}</a></h2>
    {{ project.excerpt }}
  </article>
{% endfor %}