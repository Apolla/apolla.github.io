# 宋明的博客

Hugo + [FixIt](https://github.com/hugo-fixit/FixIt) 主题，GitHub Pages 自动部署。

- 站点：https://apolla.cc
- 源码分支：`source`（Hugo 源码 + GitHub Actions 工作流）
- 发布分支：`main`（Actions 构建产物，请勿手工编辑）
- 历史备份：`legacy-site`（旧 memE 主题产物）、`master`（更早的 Gridea 站点）
- 主题：不在仓库内，CI 按固定 commit 拉取 FixIt

## 本地预览

```bash
git clone --depth 1 https://github.com/hugo-fixit/FixIt.git themes/FixIt   # 首次
sudo npm install -g sass            # Dart Sass，Hugo 编译 SCSS 需要
hugo server -D
```

## 发布

```bash
git add -A && git commit -m "post: xxx" && git push
```

推送到 `source` 即触发构建，产物自动发布到 `main`。
