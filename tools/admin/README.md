# 博客后台管理工具

apolla.cc 的本地管理后台：写文章、管分类、传项目静态包、一键构建发布，全部在浏览器里点。只监听 `127.0.0.1:8877`，不对外暴露，数据就是仓库里的文件本身——工具不引入数据库，删掉的旧东西留在 `.trash/`。

## 启动

双击仓库根目录的 **管理后台.command**，会自动起服务并打开浏览器。

也可以在终端里手动起：

     /usr/bin/python3 tools/admin/server.py            # 默认 8877
     /usr/bin/python3 tools/admin/server.py --port 9000

关掉终端窗口 = 停止服务。端口被占用时会给出提示，换 `--port` 即可。

## 四个页面

### 文章

- 左侧按分类列出全部文章，右侧编辑器改 front matter 与正文。
- `Cmd/Ctrl + S` 保存；右侧预览区实时渲染 Markdown。
- 新建文章默认 `draft: true`，本地预览能看到，正式站看不到。
- 支持改文件名/换分类（保存时自动搬文件）。

### 分类

- 一个分类 = `content/posts/<目录>/` 下的一个目录，`_index.md` 提供标题与描述。
- 新建分类时目录名只允许 `a-z 0-9 . _ -`（URL 里会带这个段）。
- 删除分类会整个目录移到 `.trash/categories/<时间戳>/`；分类下还有文章时会先确认。

### 项目页面

给 App 用的隐私政策/用户协议/支持页，放在 `static/project/<项目>/`，线上地址 `https://apolla.cc/project/<项目>/...`。

- 上传 zip：解压到 `static/project/<名字>/`，旧目录先移进 `.trash/projects/`。
  解压时剥掉 zip 里单一顶层文件夹，`../` 与绝对路径一律拒绝。
- 文件布局两种都对：
  - 平铺：`privacy.html` → `/project/<项目>/privacy.html`
  - 目录式：`privacy/index.html` → `/project/<项目>/privacy/`（**推荐**，链接更干净）
  目录式页面里引用静态资源要写 `../style.css`，别丢掉这层目录结构。
- 上传后会检查 HTML 里的相对引用能不能解析，缺文件会在结果里列出来。
- `static/` 直接映射站点根，**GitHub Pages 区分大小写**，`Plotzy` 和 `plotzy` 是两个地址。

### 发布

1. **构建**：用仓库自带的 `.tools/hugo`（0.170.0）构建到临时目录，失败就停在这一步，不会污染仓库。
2. **提交**：`git add -A` + 提交信息（默认「post: 更新站点内容」），提交前展示改了哪些文件。
3. **推送**：推到当前分支（`source`）。
4. **等 CI**：每 10 秒查一次 `git ls-remote origin main`，直到出现新的 `deploy: <sha>` 提交，最多等 6 分钟。
5. **验证**：对给出的地址挨个 curl，回报状态码和 `<title>`。

整个过程的日志在页面上实时滚，可以随时刷新页面回来看。

## URL 规则

- 文章：`/posts/<分类目录>/<slug>/`
- `slug` 优先取 front matter 里的 `slug`，没有就用 Hugo 对 `title` 的 urlize（小写、空格转 `-`、保留中文、去掉标点）。**不是文件名**，改文件名不会改 URL，改标题才会。
- 保存时如果算出来的 URL 变了，旧地址会自动写进 `aliases`，老链接靠 meta refresh 兜住（不是 301，但对读者够用）。
- 想确认某篇文章线上到底在哪：页面上的地址来自 `hugo list all` 的真实输出，可信。

## 安全边界

- 所有写操作都限制在仓库目录内，路径穿越（`../`）直接拒绝。
- 删除从不真删：一律 `mv` 到仓库根的 `.trash/<类型>/<时间戳>/`，`.gitignore` 已忽略，想找回直接搬回去。
- 不 force push，不动 `main`；`themes/ public/ resources/ .tools/` 不会被提交。
- GitHub 的 SSH 主机指纹不在 `~/.ssh/known_hosts` 时，会用 `ssh-keyscan` 生成一份放在 `.git/dsh_known_hosts`，只影响这个仓库。

## 依赖

| 依赖 | 位置 | 说明 |
| --- | --- | --- |
| python3 | 系统自带 3.9.6 | 只用标准库，无需 pip |
| hugo | `.tools/hugo` | 0.170.0，构建与预览都用它 |
| dart-sass | `.tools/dart-sass/sass` | FixIt 主题要编译 SCSS，启动时自动加进 PATH |
| git + ssh key | `~/.ssh` | 推送 `source` 用 |

系统里没有全局 `hugo` 也没关系，工具只认仓库内的那份。

## HTTP 接口

前端就是个静态页面，所有能力都在这些接口上，想用 curl / 脚本调用也行。

| 方法 | 路径 | 作用 |
| --- | --- | --- |
| GET | `/api/state` | 分支、脏文件、hugo 版本、SSH 状态、计数 |
| GET | `/api/posts?category=` | 文章列表（含真实 URL、是否被 hugo 确认） |
| GET | `/api/post?path=` | 单篇：front matter + 正文 + URL |
| GET | `/api/categories` | 分类列表（含文章数、标题、描述） |
| GET | `/api/projects` | 项目包列表（文件、页面地址、缺失引用） |
| GET | `/api/urlmap?refresh=1` | 强制刷新 `hugo list all` 的路径→URL 映射 |
| GET | `/api/preview` | 本地预览状态 |
| GET | `/api/job?id=&from=` | 任务增量日志（构建/发布） |
| POST | `/api/post/save` | 保存文章（含改名、换分类、自动 alias） |
| POST | `/api/post/new` | 新建文章 |
| POST | `/api/post/delete` | 删除文章（进 .trash） |
| POST | `/api/category/create` | 新建分类 |
| POST | `/api/category/delete` | 删除分类（进 .trash，`force` 可带文章一起） |
| POST | `/api/project/upload` | 上传项目 zip（base64） |
| POST | `/api/project/delete` | 删除项目目录（进 .trash） |
| POST | `/api/build` | 构建到临时目录，只验证不改仓库 |
| POST | `/api/preview/start` / `stop` | 起停 `hugo server`（1313） |
| POST | `/api/verify` | 批量 curl 探测线上地址 |
| POST | `/api/publish` | 构建 → 提交 → 推送 → 等 CI → 验证 |

## 常见问题

**构建报 SCSS 错误** — 主题要 dart-sass。工具启动时已经把 `.tools/dart-sass` 加进 PATH；手动跑 hugo 时也要加：

     PATH="$PWD/.tools/dart-sass:$PWD/.tools:$PATH" .tools/hugo --gc --logLevel warn

**推送报 Host key verification failed** — `github.com` 不在 `known_hosts` 里。工具会自动补一份，若仍失败：

     ssh-keyscan github.com >> ~/.ssh/known_hosts

**文章地址和预期不一样** — 看 front matter 的 `slug` 和 `title`，URL 只由这两者 + 分类目录决定。改标题会连带改地址（旧地址自动进 `aliases`）。

**发布完线上还是旧的** — GitHub Pages 有缓存。工具已经等到新的 `deploy:` 提交才开始验证，若验证 404，先确认文件是否真的进了 `main`。

**页面 404 但文件在** — 大概率大小写或目录式布局少了斜杠。目录式页面必须访问 `/xxx/` 而不是 `/xxx`。
