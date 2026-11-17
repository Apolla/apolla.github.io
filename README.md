# 宋明的博客

Hugo + [FixIt](https://github.com/hugo-fixit/FixIt) 主题，GitHub Pages 自动部署。

- 站点：<https://apolla.cc>
- 源码分支：`source`（Hugo 源码 + GitHub Actions 工作流）→ 自动构建并发布到 `main`（不要手工改）
- 历史备份：`legacy-site`（迁移前的 memE 站点）、`master`（更早的 Gridea 站点）
- 主题：不入库，CI 每次按 main 浅克隆 FixIt

## 本地预览 / 构建

```bash
git clone --depth 1 https://github.com/hugo-fixit/FixIt.git themes/FixIt   # 首次
# Dart Sass（Hugo 编译 SCSS 需要）：解压 dart-sass 到某目录并把 sass 放进 PATH
hugo server -D
hugo --gc --minify
```

## 写文章并发布

```bash
hugo new content posts/<分类>/<文件名>.md
git add -A && git commit -m "post: xxx" && git push
```

推送到 `source` 后，Actions 会自动构建并把产物发布到 `main`，稍等 1~2 分钟线上即更新。

## 目录约定

- `content/posts/<分类>/<文章>.md`：正文（front matter: title/date/categories/tags）
- `static/images/`：图片，正文用 `/images/xxx.png` 引用
- `hugo.toml`：站点配置（覆盖主题默认值）
- `static/CNAME`：自定义域名 `apolla.cc`
