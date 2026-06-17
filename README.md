# Renko PDF-first Jekyll Site

这是一个适合数学笔记发布的 GitHub Pages / Jekyll 模板。核心原则是：

- `.pdf` 是网站发布对象；
- `.tex` 是可选源码；
- 只上传 PDF，网站就会自动生成 Notes 索引；
- 不需要为每篇笔记手写 Markdown 页面。

## 你以后需要做什么

把 PDF 放进对应分类目录，然后 push 即可。

推荐目录：

```text
assets/pdf/<category>/<filename>.pdf
```

例如：

```text
assets/pdf/algebraic-geometry/sheaves.pdf
assets/pdf/representation-theory/characters.pdf
```

网站会自动显示为：

```text
Sheaves
View PDF | Download

Characters
View PDF | Download
```

## 如果也想公开 TeX 源文件

TeX 不是必须的。只有当你想让别人查看源码时，才上传同名 `.tex`：

```text
assets/tex/algebraic-geometry/sheaves.tex
```

如果 PDF 和 TeX 的 category + filename 一致，网站会自动多显示一个 `TeX` 链接：

```text
Sheaves
View PDF | Download | TeX
```

## 发布 Blog 文章

Blog 文章放在 `_posts/` 目录里，文件名必须使用 Jekyll 规定的格式：

```text
_posts/YYYY-MM-DD-english-slug.md
```

例如：

```text
_posts/2026-06-17-math-review-and-outlook.md
```

注意：

- 文件名开头必须是 `YYYY-MM-DD-`，否则 Jekyll 不会把它当作 blog 文章；
- 建议 slug 使用小写英文和连字符，不要使用空格或中文；
- 文件开头必须有 front matter，并且 `---` 必须从第一行开始；
- 如果 `date` 写在未来，GitHub Pages 默认不会显示这篇文章。

最小文章模板：

```markdown
---
layout: post
title: "文章标题"
date: 2026-06-17 20:00:00 +0800
---

这里开始写正文。
```

发布后，Blog 列表会在 `/blog/` 显示文章，文章链接通常形如：

```text
/YYYY/MM/DD/english-slug.html
```

## Blog 封面图

封面图建议放在：

```text
assets/images/blog/
```

然后在文章 front matter 里加入：

```markdown
---
layout: post
title: "文章标题"
date: 2026-06-17 20:00:00 +0800
cover: /assets/images/blog/my-cover.jpg
cover_alt: "封面说明"
cover_caption: "可选的封面题注"
---
```

说明：

- `cover` 是封面图片路径；
- `cover_alt` 是图片替代文本，建议写；
- `cover_caption` 是封面下方题注，可写可不写；
- 没有 `cover` 的文章也会正常显示，只是不显示封面。

## Blog 日期、时区和缓存

当前 `_config.yml` 里配置的是：

```yml
timezone: America/Los_Angeles
```

所以即使文章 front matter 里写了北京时间，例如：

```markdown
date: 2026-06-17 14:40:00 +0800
```

网站上也可能显示为洛杉矶日期，比如 `2026-06-16`。如果希望 Blog 日期和链接都按北京时间生成，可以改成：

```yml
timezone: Asia/Shanghai
```

如果 push 后线上暂时看不到文章，先检查：

1. GitHub Actions 是否构建成功；
2. 文章是否在 `_posts/` 目录；
3. 文件名是否是 `YYYY-MM-DD-title.md`；
4. front matter 是否从第一行开始；
5. `date` 是否不是未来时间；
6. 浏览器或 GitHub Pages 缓存是否还没刷新。

GitHub Pages 可能缓存几分钟。如果你确认线上 HTML 已经更新，但浏览器还没显示，可以尝试 `Ctrl + F5` 强制刷新，或者用无痕窗口打开。

## 已有分类目录

```text
assets/pdf/algebra/
assets/pdf/commutative-algebra/
assets/pdf/algebraic-geometry/
assets/pdf/representation-theory/
assets/pdf/homological-algebra/
assets/pdf/number-theory/
assets/pdf/analysis/
assets/pdf/misc/
```

可选 TeX 源码目录：

```text
assets/tex/algebra/
assets/tex/commutative-algebra/
assets/tex/algebraic-geometry/
assets/tex/representation-theory/
assets/tex/homological-algebra/
assets/tex/number-theory/
assets/tex/analysis/
assets/tex/misc/
```

旧版目录 `assets/notes/<category>/` 仍然兼容；但之后建议优先使用 `assets/pdf/` 和 `assets/tex/`。

## 文件命名建议

建议使用小写英文和连字符：

```text
sheaves.pdf
schemes.pdf
characters.pdf
orthogonality-relations.pdf
```

不要使用空格和中文文件名。不是不能用，而是 URL 会变得难看，也更容易出错。

## 如何部署到 GitHub Pages

1. 把这个文件夹内容放进你的 GitHub repo。
2. 进入 repo 的 Settings → Pages。
3. Build and deployment 选择 **GitHub Actions**。
4. push 到 `main` 或 `master` 分支。

GitHub Actions 会自动：

1. 扫描 `assets/pdf/` 下的 `.pdf`；
2. 扫描 `assets/tex/` 下同名 `.tex`，如果存在就附加源码链接；
3. 生成 `_data/notes.json`；
4. 构建 Jekyll 网站；
5. 部署到 GitHub Pages。

## 本地预览

安装 Ruby 和 Bundler 后运行：

```bash
bundle install
bash scripts/preview.sh
```

然后打开：

```text
http://localhost:4000
```

## 新增分类

假设你想新增 `category-theory`：

1. 新建目录：

```text
assets/pdf/category-theory/
assets/tex/category-theory/
```

2. 在 `_data/categories.yml` 里加入：

```yml
- key: category-theory
  title: Category Theory
  zh: 范畴论
  url: /notes/category-theory/
```

3. 在 `_pages/` 下新增：

```text
_pages/category-theory.md
```

内容：

```markdown
---
layout: category
title: Category Theory
category: category-theory
permalink: /notes/category-theory/
---

Category theory notes.
```

之后就可以上传：

```text
assets/pdf/category-theory/yoneda-lemma.pdf
```

如果想附源码，再上传：

```text
assets/tex/category-theory/yoneda-lemma.tex
```
