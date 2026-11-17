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
- 每个分类目录里有一个 `_index.md`，它让该目录成为独立分区，文章 URL 因此带上目录名：
  `/posts/<目录名>/<标题 slug>/`（例如 `/posts/swiftui-eul/1.4-swiftui-视图管理机制/`）。
  新增分类时记得同步创建 `_index.md`，否则该目录的文章会退回到 `/posts/<slug>/`。
- `static/images/`：图片，正文用 `/images/xxx.png` 引用
- `hugo.toml`：站点配置（覆盖主题默认值）
- `static/CNAME`：自定义域名 `apolla.cc`
- `static/project/<项目>/`：各 App 的独立页面（技术支持、隐私政策等纯静态 HTML），线上地址即 `/project/<项目>/...`
  页面既可以是扁平文件（`privacy.html` → `/project/<项目>/privacy.html`），
  也可以是目录式（`privacy/index.html` → `/project/<项目>/privacy/`），按打包产物的结构原样放即可

## 新增一个项目的支持页 / 隐私政策

以「仓鼠管家」为例，页面位于 `static/project/cangshuguanjia/`，线上地址为：

- <https://apolla.cc/project/cangshuguanjia/support.html>
- <https://apolla.cc/project/cangshuguanjia/privacy.html>

新项目（如 plotzy）按以下步骤添加：

```bash
mkdir -p static/project/plotzy
cp static/project/cangshuguanjia/support.html static/project/cangshuguanjia/privacy.html static/project/plotzy/
# 改写标题、正文、联系邮箱等项目相关文案，然后正常提交推送即可
```

约定：目录名用项目名（小写英文名，或项目自带的写法），页面文件名固定为 `support.html` 与 `privacy.html`，这样每个项目都有一对稳定可预期的 URL，方便填进 App Store Connect。

若拿到的是已打包好的站点（目录式页面），直接解压进去即可，例如「Plotzy」：

```text
static/project/Plotzy/
├── PlLegal.css
├── PlLogo.png
├── privacy/index.html
└── terms/index.html
```

线上地址：

- <https://apolla.cc/project/Plotzy/privacy/>
- <https://apolla.cc/project/Plotzy/terms/>

> `/support.html` 和 `/privacy.html` 根路径保留为跳转页（meta refresh + canonical），指向仓鼠管家的新地址，因此 App Store 中已提交的旧链接仍可正常打开。以后若某个项目长期停用，可直接删除对应目录。
