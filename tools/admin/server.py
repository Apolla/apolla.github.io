#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apolla.cc 博客后台管理工具（本地单机版）

用法：
    python3 tools/admin/server.py            # 默认 127.0.0.1:8877
    python3 tools/admin/server.py --port 9000

只监听本机回环地址，不对外暴露。所有写操作都限制在本仓库目录内。
"""

from __future__ import annotations

import base64
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import urllib.request
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT = os.path.join(ROOT, "content", "posts")
STATIC_PROJECTS = os.path.join(ROOT, "static", "project")
TRASH = os.path.join(ROOT, ".trash")
HERE = os.path.dirname(os.path.abspath(__file__))

PORT = 8877
PREVIEW_PORT = 1313

FM_ORDER = ["title", "description", "date", "lastmod", "draft",
            "categories", "tags", "weight", "slug", "aliases"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


# ---------------------------------------------------------------- 基础工具

def now_str():
    return time.strftime("%Y-%m-%dT%H:%M:%S+08:00")


def safe_path(relpath):
    """把仓库相对路径解析成绝对路径，并确保没有越界。"""
    p = os.path.abspath(os.path.join(ROOT, str(relpath)))
    if not (p == ROOT or p.startswith(ROOT + os.sep)):
        raise ValueError("路径越界：%s" % relpath)
    return p


def run(cmd, cwd=ROOT, env=None, timeout=600):
    return subprocess.run(cmd, cwd=cwd, env=env or os.environ.copy(),
                          capture_output=True, text=True, timeout=timeout)


def hugo_env():
    env = os.environ.copy()
    bins = [os.path.join(ROOT, ".tools", "dart-sass"), os.path.join(ROOT, ".tools")]
    env["PATH"] = os.pathsep.join([p for p in bins if os.path.isdir(p)] + [env.get("PATH", "")])
    return env


def hugo_bin():
    local = os.path.join(ROOT, ".tools", "hugo")
    if os.path.exists(local) and os.access(local, os.X_OK):
        return local
    return shutil.which("hugo")


def git_env():
    """让 push 可用的 SSH 环境：known_hosts 不可写时退回到仓库内的副本。"""
    env = os.environ.copy()
    kh = os.path.expanduser("~/.ssh/known_hosts")
    ok = False
    try:
        probe = subprocess.run(["ssh-keygen", "-F", "github.com", "-f", kh],
                               capture_output=True, text=True)
        ok = probe.returncode == 0
    except Exception:
        ok = False
    if not ok:
        alt = os.path.join(ROOT, ".git", "dsh_known_hosts")
        try:
            if not os.path.exists(alt) or os.path.getsize(alt) == 0:
                scan = subprocess.run(["ssh-keyscan", "-t", "rsa,ecdsa,ed25519", "github.com"],
                                      capture_output=True, timeout=30)
                os.makedirs(os.path.dirname(alt), exist_ok=True)
                with open(alt, "wb") as fh:
                    fh.write(scan.stdout)
            if os.path.getsize(alt) > 0:
                env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=%s" % alt
        except Exception:
            pass
    return env


def ssh_state():
    kh = os.path.expanduser("~/.ssh/known_hosts")
    try:
        probe = subprocess.run(["ssh-keygen", "-F", "github.com", "-f", kh],
                               capture_output=True, text=True)
        return {"ready": probe.returncode == 0, "knownHosts": kh,
                "note": "" if probe.returncode == 0 else "github.com 不在 known_hosts，将使用仓库内副本"}
    except Exception as exc:
        return {"ready": False, "knownHosts": kh, "note": str(exc)}


# ---------------------------------------------------------- front matter

def split_front_matter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, text


def _unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        q, body = s[0], s[1:-1]
        if q == '"':
            return body.replace('\\"', '"').replace('\\\\', '\\')
        return body.replace("''", "'")
    return s


def _inline_list(s):
    s = s.strip()
    if not (s.startswith("[") and s.endswith("]")):
        return []
    body = s[1:-1].strip()
    if not body:
        return []
    out, cur, quote_ch = [], "", None
    for ch in body:
        if quote_ch:
            if ch == quote_ch:
                quote_ch = None
            else:
                cur += ch
        elif ch in "\"'":
            quote_ch = ch
        elif ch == ",":
            v = cur.strip()
            if v:
                out.append(v)
            cur = ""
        else:
            cur += ch
    v = cur.strip()
    if v:
        out.append(v)
    return out


def parse_front_matter(raw):
    data, extras, key = {}, [], None
    for line in (raw or "").split("\n"):
        if not line.strip():
            continue
        if line[0] in " \t":
            item = line.strip()
            if key is not None and item.startswith("- ") and isinstance(data.get(key), list):
                data[key].append(_unquote(item[2:]))
            else:
                extras.append(line)
            continue
        if ":" not in line:
            extras.append(line)
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        key = k
        if v == "":
            data[k] = []
        elif v.startswith("["):
            data[k] = _inline_list(v)
        elif v.lower() in ("true", "false"):
            data[k] = v.lower() == "true"
        else:
            data[k] = _unquote(v)
    return data, extras


def _q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def dump_front_matter(data, extras=None):
    lines = []
    order = [k for k in FM_ORDER if k in data] + [k for k in data if k not in FM_ORDER]
    for k in order:
        v = data[k]
        if isinstance(v, bool):
            lines.append("%s: %s" % (k, "true" if v else "false"))
        elif isinstance(v, list):
            if k == "aliases":
                if v:
                    lines.append("aliases:")
                    for item in v:
                        lines.append("  - " + _q(item))
                else:
                    lines.append("aliases: []")
            else:
                lines.append("%s: [%s]" % (k, ", ".join(_q(x) for x in v)))
        elif isinstance(v, int):
            lines.append("%s: %d" % (k, v))
        else:
            s = str(v).strip()
            if not s:
                continue
            if DATE_RE.match(s) or re.match(r"^\d+(\.\d+)?$", s):
                lines.append("%s: %s" % (k, s))
            else:
                lines.append("%s: %s" % (k, _q(s)))
    if extras:
        lines.extend([x for x in extras if x.strip()])
    return "\n".join(lines)


def urlize(text):
    out = []
    for ch in str(text):
        if ch.isspace():
            out.append("-")
        elif ch.isalnum() or ch in ".-_":
            out.append(ch.lower())
    slug = re.sub(r"-{2,}", "-", "".join(out)).strip("-")
    return slug


def post_url(category, data):
    slug = str(data.get("slug") or "").strip() or urlize(str(data.get("title") or ""))
    return "/posts/%s/%s/" % (category, slug)


def enc_url(path):
    """把含中文的地址转成线上实际使用的百分号编码形式（仅用于展示/校验）。"""
    return quote(str(path), safe="/")


def read_post(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    raw, body = split_front_matter(text)
    data, extras = parse_front_matter(raw or "")
    return text, raw, body, data, extras


def write_post(path, data, extras, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fm = dump_front_matter(data, extras)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("---\n" + fm + "\n---\n" + body)


# ---------------------------------------------------------------- 内容读取

def _md_files():
    out = []
    for base, _dirs, files in os.walk(CONTENT):
        for f in files:
            if f.endswith(".md"):
                out.append(os.path.join(base, f))
    return out


_urlmap_cache = {"key": None, "map": {}}


def build_urlmap(force=False):
    hb = hugo_bin()
    if not hb:
        return {}
    files = _md_files()
    key = str(max([os.path.getmtime(f) for f in files] + [0]))
    if not force and _urlmap_cache["key"] == key:
        return _urlmap_cache["map"]
    mapping = {}
    try:
        proc = run([hb, "list", "all"], env=hugo_env(), timeout=300)
        if proc.returncode == 0:
            for row in csv.DictReader(io.StringIO(proc.stdout)):
                path = (row.get("path") or "").replace(os.sep, "/")
                perm = row.get("permalink") or ""
                if path and perm:
                    mapping[path] = urlparse(perm).path
    except Exception:
        mapping = {}
    _urlmap_cache.update(key=key, map=mapping)
    return mapping


def list_categories():
    out = []
    if not os.path.isdir(CONTENT):
        return out
    for name in sorted(os.listdir(CONTENT)):
        d = os.path.join(CONTENT, name)
        if not os.path.isdir(d):
            continue
        posts = [f for f in os.listdir(d) if f.endswith(".md") and f != "_index.md"]
        idx = os.path.join(d, "_index.md")
        title = desc = ""
        has_index = os.path.exists(idx)
        if has_index:
            try:
                _text, _raw, _body, data, _ex = read_post(idx)
                title = str(data.get("title") or "")
                desc = str(data.get("description") or "")
            except Exception:
                pass
        out.append({"dir": name, "count": len(posts), "hasIndex": has_index,
                    "title": title, "description": desc})
    return out


def list_posts(category=None):
    mapping = build_urlmap()
    out = []
    if not os.path.isdir(CONTENT):
        return out
    for dirname in sorted(os.listdir(CONTENT)):
        d = os.path.join(CONTENT, dirname)
        if not os.path.isdir(d):
            continue
        if category and dirname != category:
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".md") or name == "_index.md":
                continue
            ap = os.path.join(d, name)
            try:
                text, _raw, body, data, _ex = read_post(ap)
            except Exception as exc:
                out.append({"path": "content/posts/%s/%s" % (dirname, name),
                            "error": str(exc)})
                continue
            relp = "content/posts/%s/%s" % (dirname, name)
            real = mapping.get(relp)
            out.append({
                "path": relp,
                "file": name,
                "category": dirname,
                "title": str(data.get("title") or name[:-3]),
                "date": str(data.get("date") or ""),
                "lastmod": str(data.get("lastmod") or ""),
                "draft": bool(data.get("draft")),
                "tags": data.get("tags") if isinstance(data.get("tags"), list) else [],
                "categories": data.get("categories") if isinstance(data.get("categories"), list) else [],
                "weight": data.get("weight"),
                "aliases": data.get("aliases") if isinstance(data.get("aliases"), list) else [],
                "url": real or enc_url(post_url(dirname, data)),
                "urlVerified": bool(real),
                "chars": len(body or ""),
                "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(ap))),
            })
    return out


# ---------------------------------------------------------------- 项目页面

def _project_info(name):
    d = os.path.join(STATIC_PROJECTS, name)
    pages, assets, files = [], [], []
    total = 0
    for base, _dirs, fs in os.walk(d):
        for f in sorted(fs):
            ap = os.path.join(base, f)
            relp = os.path.relpath(ap, d).replace(os.sep, "/")
            size = os.path.getsize(ap)
            total += size
            files.append({"path": relp, "size": size})
            if f.endswith(".html"):
                if relp == "index.html":
                    url = "/project/%s/" % name
                elif relp.endswith("/index.html"):
                    sub = relp[: -len("/index.html")].strip("/")
                    url = "/project/%s/%s/" % (name, sub)
                else:
                    url = "/project/%s/%s" % (name, relp)
                pages.append({"path": relp, "url": url})
            else:
                assets.append(relp)
    return {"name": name, "files": files, "pages": pages, "assets": assets, "bytes": total}


def list_projects():
    out = []
    if not os.path.isdir(STATIC_PROJECTS):
        return out
    for name in sorted(os.listdir(STATIC_PROJECTS)):
        d = os.path.join(STATIC_PROJECTS, name)
        if os.path.isdir(d):
            try:
                out.append(_project_info(name))
            except Exception:
                pass
    return out


def _check_refs(root, name):
    """检查 html 里的相对引用能否解析，返回缺失清单。"""
    missing = []
    for base, _dirs, fs in os.walk(root):
        for f in fs:
            if not f.endswith(".html"):
                continue
            ap = os.path.join(base, f)
            try:
                text = open(ap, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
                val = m.group(1).strip()
                if not val or val.startswith(("http://", "https://", "//", "#", "mailto:", "tel:", "javascript:", "data:")):
                    continue
                target = os.path.normpath(os.path.join(os.path.dirname(ap), val.split("#")[0].split("?")[0]))
                if not (target == root or target.startswith(root + os.sep)):
                    missing.append({"file": os.path.relpath(ap, root), "ref": val, "reason": "越出项目目录"})
                elif not os.path.exists(target):
                    missing.append({"file": os.path.relpath(ap, root), "ref": val, "reason": "文件不存在"})
    return missing


def _validate_project_name(name):
    name = str(name or "").strip()
    if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$", name):
        raise ValueError("项目名只能用字母数字和 . _ -（如 Plotzy、cangshuguanjia）")
    return name


def upload_project(name, b64):
    name = _validate_project_name(name)
    raw = base64.b64decode(b64)
    tmp = tempfile.mkdtemp(prefix="adminzip-")
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                target = os.path.abspath(os.path.join(tmp, info.filename))
                if not target.startswith(tmp + os.sep):
                    raise ValueError("压缩包含非法路径：%s" % info.filename)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with zf.open(info) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
        entries = [e for e in os.listdir(tmp)]
        src_root = tmp
        if len(entries) == 1 and os.path.isdir(os.path.join(tmp, entries[0])):
            src_root = os.path.join(tmp, entries[0])
        dest = os.path.join(STATIC_PROJECTS, name)
        if os.path.exists(dest):
            archive_path = os.path.join(TRASH, "projects", time.strftime("%Y%m%d-%H%M%S"), name)
            os.makedirs(os.path.dirname(archive_path), exist_ok=True)
            shutil.move(dest, archive_path)
        os.makedirs(STATIC_PROJECTS, exist_ok=True)
        shutil.move(src_root, dest)
        info = _project_info(name)
        info["missing"] = _check_refs(dest, name)
        return info
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def delete_project(name):
    name = _validate_project_name(name)
    dest = os.path.join(STATIC_PROJECTS, name)
    if not os.path.isdir(dest):
        raise ValueError("项目不存在：%s" % name)
    archive_path = os.path.join(TRASH, "projects", time.strftime("%Y%m%d-%H%M%S"), name)
    os.makedirs(os.path.dirname(archive_path), exist_ok=True)
    shutil.move(dest, archive_path)
    return {"movedTo": os.path.relpath(archive_path, ROOT)}


# ---------------------------------------------------------------- 任务与进程

class Job(object):
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.state = "running"
        self.ok = None
        self.extra = {}
        self.started = time.time()
        self.lock = threading.Lock()

    def log(self, msg):
        with self.lock:
            stamp = time.strftime("%H:%M:%S")
            for line in str(msg).rstrip("\n").split("\n"):
                self.lines.append("[%s] %s" % (stamp, line))
            if len(self.lines) > 800:
                del self.lines[: len(self.lines) - 800]

    def finish(self, ok, **extra):
        self.ok = ok
        self.state = "done"
        self.extra.update(extra)

    def snapshot(self, from_index=0):
        with self.lock:
            return {"id": self.name, "state": self.state, "ok": self.ok,
                    "lines": self.lines[from_index:], "total": len(self.lines),
                    "elapsed": round(time.time() - self.started, 1),
                    "extra": self.extra}


_jobs = {}
_jobs_lock = threading.Lock()


def new_job(name):
    job = Job(name + "-" + time.strftime("%H%M%S"))
    with _jobs_lock:
        _jobs[job.name] = job
        if len(_jobs) > 20:
            for k in list(_jobs)[:-20]:
                _jobs.pop(k, None)
    return job


def get_job(job_id):
    with _jobs_lock:
        return _jobs.get(job_id)


def current_branch():
    proc = run(["git", "branch", "--show-current"])
    return proc.stdout.strip() or "source"


def git_status():
    env = git_env()
    proc = run(["git", "status", "--porcelain"], env=env)
    lines = [l for l in proc.stdout.split("\n") if l.strip()]
    return {"branch": current_branch(), "dirty": len(lines), "entries": lines[:80],
            "lastCommit": run(["git", "log", "-1", "--pretty=%h %s"], env=env).stdout.strip()}


def do_build(job=None):
    hb = hugo_bin()
    if not hb:
        raise RuntimeError("未找到 hugo 可执行文件（.tools/hugo）")
    out_dir = os.path.join(tempfile.gettempdir(), "blog-admin-build")
    shutil.rmtree(out_dir, ignore_errors=True)
    proc = run([hb, "--gc", "--logLevel", "warn", "-d", out_dir, "--cleanDestinationDir"],
               env=hugo_env(), timeout=900)
    ok = proc.returncode == 0 and os.path.exists(os.path.join(out_dir, "index.html"))
    detail = (proc.stdout + proc.stderr).strip()
    if job:
        job.log("hugo 构建：" + ("成功" if ok else "失败"))
        if detail:
            job.log(detail[-3000:])
    return {"ok": ok, "output": detail[-4000:], "dir": out_dir}


def deploy_head():
    proc = run(["git", "ls-remote", "origin", "main"], env=git_env(), timeout=120)
    parts = proc.stdout.split()
    return parts[0] if parts else ""


def do_publish(job, message, verify_urls):
    env = git_env()
    job.log("① 构建检查（失败会中止发布）")
    build = do_build(job)
    if not build["ok"]:
        job.log("构建未通过，已中止，未提交任何改动")
        job.finish(False, stage="build", output=build["output"][-3000:])
        return

    branch = current_branch()
    status = run(["git", "status", "--porcelain"], env=env).stdout.strip()
    if not status:
        job.log("工作区干净，没有需要提交的改动")
        job.finish(True, stage="noop", branch=branch)
        return
    job.log("待提交文件：\n" + status)

    before = deploy_head()
    job.log("② 提交")
    run(["git", "add", "-A"], env=env)
    diffstat = run(["git", "diff", "--cached", "--stat"], env=env).stdout.strip()
    if diffstat:
        job.log(diffstat)
    msg = (message or "").strip() or "post: 更新站点内容"
    commit = run(["git", "commit", "-m", msg], env=env)
    job.log((commit.stdout + commit.stderr).strip()[-2000:])
    if commit.returncode != 0:
        job.finish(False, stage="commit")
        return

    job.log("③ 推送到 " + branch)
    push = run(["git", "push", "origin", branch], env=env, timeout=600)
    job.log((push.stdout + push.stderr).strip()[-2000:])
    if push.returncode != 0:
        job.log("推送失败")
        job.finish(False, stage="push")
        return

    job.log("④ 等待 GitHub Actions 部署（最长 6 分钟）")
    deployed = ""
    deadline = time.time() + 360
    while time.time() < deadline:
        time.sleep(10)
        head = deploy_head()
        if head and head != before:
            deployed = head
            job.log("main 已更新：" + head[:7])
            break
        job.log("…仍在构建")
    if not deployed:
        job.log("等待超时，请到 Actions 页面确认")
        job.finish(False, stage="deploy")

    job.log("⑤ 校验线上地址")
    results = []
    urls = [u for u in (verify_urls or []) if u]
    if not urls:
        urls = ["https://apolla.cc/"]
    for u in urls:
        results.append(http_probe(u))
        job.log("%s → %s" % (u, results[-1].get("status")))
    ok = all(str(r.get("status")) == "200" for r in results)
    job.finish(ok, stage="done", deployHead=deployed[:7], checks=results)


def http_probe(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "blog-admin/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(200000).decode("utf-8", "replace")
            m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
            return {"url": url, "status": resp.status,
                    "title": (m.group(1).strip() if m else "")[:120]}
    except urllib.error.HTTPError as exc:
        return {"url": url, "status": exc.code, "title": ""}
    except Exception as exc:
        return {"url": url, "status": "ERR", "title": str(exc)[:120]}


_preview = {"proc": None, "port": PREVIEW_PORT}


def preview_status():
    proc = _preview["proc"]
    running = bool(proc and proc.poll() is None)
    return {"running": running, "url": "http://127.0.0.1:%d/" % _preview["port"] if running else "",
            "port": _preview["port"]}


def preview_start():
    hb = hugo_bin()
    if not hb:
        raise RuntimeError("未找到 hugo 可执行文件")
    st = preview_status()
    if st["running"]:
        return st
    log_path = os.path.join(tempfile.gettempdir(), "blog-admin-hugo-server.log")
    fh = open(log_path, "w", encoding="utf-8")
    proc = subprocess.Popen([hb, "server", "--bind", "127.0.0.1", "--port", str(PREVIEW_PORT),
                             "-D", "--disableFastRender", "--noHTTPCache"],
                            cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT, env=hugo_env())
    _preview["proc"] = proc
    for _ in range(60):
        time.sleep(0.5)
        if proc.poll() is not None:
            break
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/" % PREVIEW_PORT, timeout=2) as r:
                if r.status == 200:
                    return {"running": True, "url": "http://127.0.0.1:%d/" % PREVIEW_PORT,
                            "port": PREVIEW_PORT, "log": log_path}
        except Exception:
            continue
    st = preview_status()
    st["log"] = log_path
    return st


def preview_stop():
    proc = _preview["proc"]
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
    _preview["proc"] = None
    return {"running": False}


# ---------------------------------------------------------------- 写操作

def save_post(payload):
    relpath = str(payload.get("path") or "").strip()
    if not relpath.startswith("content/posts/"):
        raise ValueError("只能编辑 content/posts/ 下的文章")
    ap = safe_path(relpath)
    exists = os.path.exists(ap)
    old_data, old_body, old_url, old_extras = {}, "", "", []
    if exists:
        _text, _raw, old_body, old_data, old_extras = read_post(ap)

    category = relpath.split("/")[2]
    new_rel = str(payload.get("newPath") or "").strip() or relpath
    if not new_rel.startswith("content/posts/"):
        raise ValueError("目标路径非法")
    category = new_rel.split("/")[2]

    data = {}
    title = str(payload.get("title") or "").strip()
    if not title:
        raise ValueError("标题不能为空")
    data["title"] = title
    desc = str(payload.get("description") or "").strip()
    if desc:
        data["description"] = desc
    date = str(payload.get("date") or "").strip() or now_str()
    data["date"] = date
    data["lastmod"] = str(payload.get("lastmod") or "").strip() or now_str()
    data["draft"] = bool(payload.get("draft"))
    cats = [c.strip() for c in (payload.get("categories") or []) if str(c).strip()]
    if cats:
        data["categories"] = cats
    tags = [t.strip() for t in (payload.get("tags") or []) if str(t).strip()]
    if tags:
        data["tags"] = tags
    weight = payload.get("weight")
    if weight not in (None, "", []):
        try:
            data["weight"] = int(weight)
        except Exception:
            pass

    aliases = [a for a in (payload.get("aliases") or []) if str(a).strip()]
    if exists:
        old_aliases = old_data.get("aliases") if isinstance(old_data.get("aliases"), list) else []
        for a in old_aliases:
            if a not in aliases:
                aliases.append(a)
        old_url = post_url(relpath.split("/")[2], old_data)
    new_url = post_url(category, data)
    if old_url and old_url != new_url and old_url not in aliases:
        aliases.insert(0, old_url)
    if aliases:
        data["aliases"] = aliases

    body = payload.get("body")
    if body is None:
        body = old_body
    body = str(body)
    if not body.startswith("\n"):
        body = "\n" + body

    target = safe_path(new_rel)
    if exists and target != ap:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        os.replace(ap, target)
    write_post(target, data, old_extras, body)
    return {"path": new_rel, "url": enc_url(new_url), "aliases": aliases,
            "oldUrl": enc_url(old_url) if old_url and old_url != new_url else ""}


def delete_post(relpath):
    if not str(relpath).startswith("content/posts/"):
        raise ValueError("只能删除 content/posts/ 下的文章")
    ap = safe_path(relpath)
    if not os.path.exists(ap):
        raise ValueError("文件不存在")
    dest = os.path.join(TRASH, "posts", time.strftime("%Y%m%d-%H%M%S"), relpath)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(ap, dest)
    return {"movedTo": os.path.relpath(dest, ROOT)}


def create_category(payload):
    name = str(payload.get("dir") or "").strip()
    if not re.match(r"^[a-z0-9][a-z0-9._-]{0,63}$", name):
        raise ValueError("分类目录名只能用 a-z 0-9 . _ -（如 swiftui-eul）")
    d = os.path.join(CONTENT, name)
    if os.path.isdir(d):
        raise ValueError("分类已存在：%s" % name)
    os.makedirs(d)
    data = {"title": str(payload.get("title") or name).strip(),
            "draft": False}
    desc = str(payload.get("description") or "").strip()
    if desc:
        data["description"] = desc
    write_post(os.path.join(d, "_index.md"), data, [], "\n")
    return {"dir": name}


def delete_category(payload):
    name = str(payload.get("dir") or "").strip()
    if not re.match(r"^[a-z0-9][a-z0-9._-]{0,63}$", name):
        raise ValueError("分类目录名非法")
    d = os.path.join(CONTENT, name)
    if not os.path.isdir(d):
        raise ValueError("分类不存在：%s" % name)
    others = [f for f in os.listdir(d) if f != "_index.md"]
    if others and not payload.get("force"):
        raise ValueError("该分类下还有 %d 个文件，确认要一起删除再重试" % len(others))
    dest = os.path.join(TRASH, "categories", time.strftime("%Y%m%d-%H%M%S"), name)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(d, dest)
    return {"dir": name, "movedTo": os.path.relpath(dest, ROOT), "files": len(others)}


def create_post(payload):
    category = str(payload.get("category") or "").strip()
    if not category:
        raise ValueError("请选择分类")
    d = os.path.join(CONTENT, category)
    if not os.path.isdir(d):
        raise ValueError("分类目录不存在：%s" % category)
    title = str(payload.get("title") or "").strip() or "未命名文章"
    fname = str(payload.get("file") or "").strip() or (urlize(title) or "untitled") + ".md"
    if not fname.endswith(".md"):
        fname += ".md"
    if os.path.exists(os.path.join(d, fname)):
        raise ValueError("同名文件已存在：%s" % fname)
    data = {"title": title, "date": now_str(), "lastmod": now_str(), "draft": True}
    cats = payload.get("categories") or []
    if cats:
        data["categories"] = [c for c in cats if str(c).strip()]
    write_post(os.path.join(d, fname), data, [], "\n<br>\n\n")
    return {"path": "content/posts/%s/%s" % (category, fname)}


def repo_state():
    hb = hugo_bin()
    st = git_status()
    st.update({
        "root": ROOT,
        "hugo": {"path": hb or "", "ok": bool(hb),
                 "version": (run([hb, "version"]).stdout.split("\n")[0] if hb else "")},
        "ssh": ssh_state(),
        "preview": preview_status(),
        "counts": {"posts": len([p for p in list_posts() if not p.get("error")]),
                   "categories": len(list_categories()),
                   "projects": len(list_projects())},
    })
    return st


# ---------------------------------------------------------------- HTTP

MAX_BODY = 80 * 1024 * 1024


class Handler(BaseHTTPRequestHandler):
    server_version = "BlogAdmin/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    # --- 响应工具
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, obj)

    def _err(self, exc, code=400):
        self._json({"ok": False, "error": str(exc)}, code)

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        if length > MAX_BODY:
            raise ValueError("请求体过大")
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    # --- 路由
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        try:
            if path in ("/", "/index.html"):
                with open(os.path.join(HERE, "ui.html"), "rb") as fh:
                    return self._send(200, fh.read(), "text/html; charset=utf-8")
            if path == "/favicon.ico":
                return self._send(204, b"", "image/x-icon")
            if path == "/api/state":
                return self._json(repo_state())
            if path == "/api/categories":
                return self._json({"items": list_categories()})
            if path == "/api/posts":
                cat = (qs.get("category") or [None])[0]
                return self._json({"items": list_posts(cat)})
            if path == "/api/post":
                relp = (qs.get("path") or [""])[0]
                if not relp.startswith("content/posts/"):
                    raise ValueError("路径非法")
                ap = safe_path(relp)
                if not os.path.exists(ap):
                    raise ValueError("文件不存在")
                _text, raw, body, data, extras = read_post(ap)
                cat = relp.split("/")[2]
                mapping = build_urlmap()
                return self._json({"path": relp, "frontMatter": data, "body": body,
                                   "extras": extras, "url": mapping.get(relp) or enc_url(post_url(cat, data)),
                                   "urlVerified": relp in mapping})
            if path == "/api/urlmap":
                force = (qs.get("refresh") or ["0"])[0] == "1"
                return self._json({"map": build_urlmap(force), "size": len(build_urlmap(force))})
            if path == "/api/projects":
                return self._json({"items": list_projects()})
            if path == "/api/git/status":
                return self._json(git_status())
            if path == "/api/job":
                job = get_job((qs.get("id") or [""])[0])
                if not job:
                    raise ValueError("任务不存在")
                start = int((qs.get("from") or ["0"])[0])
                return self._json(job.snapshot(start))
            if path == "/api/preview":
                return self._json(preview_status())
            return self._err("未知接口", 404)
        except ValueError as exc:
            return self._err(exc, 400)
        except Exception as exc:
            traceback.print_exc()
            return self._err(exc, 500)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            payload = self._body()
            if path == "/api/post/save":
                return self._json(save_post(payload))
            if path == "/api/post/new":
                return self._json(create_post(payload))
            if path == "/api/post/delete":
                return self._json(delete_post(payload.get("path")))
            if path == "/api/category/create":
                return self._json(create_category(payload))
            if path == "/api/category/delete":
                return self._json(delete_category(payload))
            if path == "/api/project/upload":
                return self._json(upload_project(payload.get("name"), payload.get("zip") or ""))
            if path == "/api/project/delete":
                return self._json(delete_project(payload.get("name")))
            if path == "/api/build":
                return self._json(do_build())
            if path == "/api/preview/start":
                return self._json(preview_start())
            if path == "/api/preview/stop":
                return self._json(preview_stop())
            if path == "/api/verify":
                urls = payload.get("urls") or []
                return self._json({"checks": [http_probe(u) for u in urls]})
            if path == "/api/publish":
                job = new_job("publish")
                threading.Thread(target=_publish_wrapper,
                                 args=(job, payload.get("message"), payload.get("urls") or []),
                                 daemon=True).start()
                return self._json({"job": job.name})
            return self._err("未知接口", 404)
        except ValueError as exc:
            return self._err(exc, 400)
        except Exception as exc:
            traceback.print_exc()
            return self._err(exc, 500)


def _publish_wrapper(job, message, urls):
    try:
        do_publish(job, message, urls)
    except Exception as exc:
        job.log("异常：%s" % exc)
        job.log(traceback.format_exc()[-2000:])
        job.finish(False, stage="exception")


def main():
    global PORT
    argv = sys.argv[1:]
    if "--port" in argv:
        PORT = int(argv[argv.index("--port") + 1])
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    httpd.daemon_threads = True
    print("博客后台已启动：http://127.0.0.1:%d" % PORT)
    print("仓库：%s" % ROOT)
    print("按 Ctrl+C 停止")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
    finally:
        preview_stop()


if __name__ == "__main__":
    main()
