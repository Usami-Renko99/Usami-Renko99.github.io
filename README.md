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
