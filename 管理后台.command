#!/bin/bash
# apolla.cc 博客管理后台 —— 双击即可打开
# 只监听本机 127.0.0.1，不对外暴露；关闭这个终端窗口就停止服务。

cd "$(dirname "$0")" || exit 1

PORT="${PORT:-8877}"
URL="http://127.0.0.1:${PORT}/"

if ! /usr/bin/python3 -c "import sys" 2>/dev/null; then
  echo "找不到 python3，请先安装 Xcode 命令行工具：xcode-select --install"
  read -r -n 1 -p "按任意键退出..."
  exit 1
fi

if curl -s -o /dev/null -m 2 "$URL"; then
  echo "管理后台已经在运行，直接打开浏览器：$URL"
  open "$URL"
  exit 0
fi

echo "正在启动 apolla.cc 管理后台（端口 ${PORT}）..."
/usr/bin/python3 tools/admin/server.py --port "$PORT" &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null' EXIT INT TERM

for _ in $(seq 1 60); do
  if curl -s -o /dev/null -m 1 "$URL"; then
    open "$URL"
    break
  fi
  sleep 0.5
done

echo
echo "后台地址：$URL        （关掉这个窗口即停止服务）"
echo
wait "$SERVER_PID"
