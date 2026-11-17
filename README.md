# 宋明的博客

Hugo + [FixIt](https://github.com/hugo-fixit/FixIt) 主题，GitHub Pages 部署。

- 站点域名：https://apolla.cc
- 源码分支：`source`（Hugo 源码 + Actions 工作流）
- 发布分支：`main`（由 Actions 构建产物自动推送，请勿手工编辑）
- 历史站点备份：`legacy-site`（旧 memE 主题产物）、`master`（更早的 Gridea 站点）

## 本地开发

```bash
# Hugo 0.170+ (标准版即可) 与 Dart Sass
export PATH="$PWD/.tools/dart-sass:$PATH"
.tools/hugo server -D
```

## 构建

```bash
export PATH="$PWD/.tools/dart-sass:$PATH"
.tools/hugo --gc --minify
```

## 发布

推送到 `source` 分支即触发 Actions，构建结果自动发布到 `main`。

## 文章

文章位于 `content/posts/<分类英文名>/<slug>.md`，图片位于 `static/images/`。
