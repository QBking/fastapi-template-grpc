#!/bin/bash
set -euo pipefail

MODE="dev"

# 参数解析
while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--dev) MODE="dev"; shift ;;
    -p|--prod) MODE="prod"; shift ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

# 加载环境变量
ENV_FILE=".env.${MODE}"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "错误: 环境变量文件 $ENV_FILE 不存在。"
  exit 1
fi

export ENV="$MODE"
set -a
source "$ENV_FILE"
set +a

echo "尝试停止 ${MODE} 模式的服务 (端口: $PORT)..."

pid=""

# 查找进程
pid=$(lsof -t -i :"$PORT" -sTCP:LISTEN 2>/dev/null || echo "")
if [[ -z "$pid" ]]; then
    pid=$(ps aux | grep "uvicorn" | grep "$PORT" | grep -v grep | awk '{print $2}' || echo "")
fi

if [[ -z "$pid" ]]; then
    echo "没有找到运行在端口 $PORT 的服务"
    exit 0
fi

echo "找到 uvicorn 进程 PID=${pid}，发送 SIGINT..."

# 循环给每个 PID 发送 SIGINT
for p in $pid; do
    kill -INT "$p"
done

# 等待最多 5 秒，检查所有 PID 是否都退出
for i in {1..5}; do
    all_exited=true
    for p in $pid; do
        if kill -0 "$p" 2>/dev/null; then
            all_exited=false
            break
        fi
    done
    if $all_exited; then
        echo "服务已优雅停止"
        exit 0
    fi
    sleep 1
done

# 5 秒还没退出，强制 kill
echo "进程 $pid 未在 5 秒内退出，执行强制 kill"
for p in $pid; do
    kill -9 "$p"
done