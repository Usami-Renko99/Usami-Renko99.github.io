---
layout: page
title: Blog
permalink: /blog/
---

{% if site.posts.size > 0 %}
  <ul class="post-list">
    {% for post in site.posts %}
      <li>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        <span class="meta">{{ post.date | date: "%Y-%m-%d" }}</span>
      </li>
    {% endfor %}
  </ul>
{% else %}
  <p>暂时还没有文章。</p>
{% endif %}
