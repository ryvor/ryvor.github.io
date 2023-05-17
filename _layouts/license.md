---
# Copyright (c) 2018 Florian Klampfer <https://qwtel.com/>
layout: base
---

{% assign version = jekyll.version | split:'.' %}
{% assign major = version[0] | plus:0 %}
{% assign minor = version[1] | plus:0 %}
{% assign patch = version[2] | plus:0 %}

{% if major >= 4 and minor >= 1 %}
  {% assign parent = site.pages | find:"show_collection",license.collection %}
{% else %}
  {% assign parent = site.pages | where:"show_collection",license.collection | first %}
{% endif %}

{% include_cached components/license.html post=page no_link_title=true no_excerpt=true hide_image=page.hide_image hide_description=page.hide_description parent=parent %}

{% include components/dingbat.html %}