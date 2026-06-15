# Renko的完美算数教室

这是一个基于 GitHub Pages + Jekyll + minima 的个人网站模板。

## 本地预览

```bash
bundle install
bundle exec jekyll serve
```

然后打开：

```text
http://localhost:4000
```

## 目录结构

```text
.
├── _config.yml
├── index.md
├── about.md
├── blog.md
├── notes.md
├── _notes/
├── _posts/
├── _layouts/
├── _includes/
└── assets/
```

## 写数学笔记

在 `_notes/` 下创建 Markdown 文件，例如：

```text
_notes/representation/schur-lemma.md
```

文件头格式：

```yaml
---
title: Schur's Lemma
topic: Representation Theory
order: 2
tags: [finite-groups]
summary: "Schur 引理及其在表示论中的作用。"
---
```

## 写博客

在 `_posts/` 下创建文章，文件名格式必须是：

```text
YYYY-MM-DD-title.md
```
