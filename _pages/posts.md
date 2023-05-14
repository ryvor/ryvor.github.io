---
layout: blog
title: Posts
description: All posts by year of publication.
permalink: /Posts/
cover: false
---

<ul>
    {% for category in site.categories %}
        <li><a name="{{ category | posts }}">{{ category | posts }}</a>
            <ul>
                {% for post in category.last %}
                    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
                {% endfor %}
            </ul>
        </li>
    {% endfor %}
</ul>