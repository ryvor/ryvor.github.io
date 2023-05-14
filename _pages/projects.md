---
layout:    default
title:     "My Projects"
permalink: /Projects/
---

{% for project in site.projects %}
  <article>
    <h2><a href="{{ project.url }}">{{ project.title }}</a></h2>
    {{ project.excerpt }}
  </article>
{% endfor %}