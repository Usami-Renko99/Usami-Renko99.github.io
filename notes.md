---
layout: page
title: Notes
permalink: /notes/
---

# Notes

这里整理长期维护的数学笔记。笔记不追求一次写完，而是会随着学习不断修订。

{% assign grouped_notes = site.notes | group_by: "topic" %}
{% for group in grouped_notes %}
## {{ group.name | default: "Uncategorized" }}

{% assign sorted_notes = group.items | sort: "order" %}
{% for note in sorted_notes %}
- [{{ note.title }}]({{ note.url | relative_url }}){% if note.summary %} — {{ note.summary }}{% endif %}
{% endfor %}

{% endfor %}
