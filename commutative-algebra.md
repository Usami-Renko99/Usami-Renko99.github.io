<!doctype html>
<html lang="{{ site.lang | default: 'zh-CN' }}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% if page.title %}{{ page.title }} · {% endif %}{{ site.title }}</title>
    <meta name="description" content="{{ page.description | default: site.description | escape }}">
    <link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">
    {% include mathjax.html %}
  </head>
  <body>
    <header class="site-header">
      <div class="container header-inner">
        <a class="site-title" href="{{ '/' | relative_url }}">{{ site.title }}</a>
        {% include nav.html %}
      </div>
    </header>

    <main class="container page-content">
      {{ content }}
    </main>

    <footer class="site-footer">
      <div class="container">
        <p>Powered by Jekyll · TeX-first notes archive</p>
      </div>
    </footer>
  </body>
</html>
