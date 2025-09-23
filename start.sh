#!/bin/bash

# start.sh - 用于启动 Uvicorn 服务的脚本
#
# 用法:
#   ./start.sh [模式] [方式]
#
# 参数:
#   模式:
#     -d, --dev       开发模式。使用 .env.dev 配置文件。如果 DEBUG=True 则启用热重载。
#     -p, --prod      生产模式。使用 .env.prod 配置文件。
#
#   方式:
#     -b, --background  后台运行。将日志输出到 logs/app.log 和 logs/app.err 文件中。
#
# 示例:
#   ./start.sh -p          # 以生产模式在前台启动
#   ./start.sh -b          # 以开发模式在后台启动
#   ./start.sh -p -b       # 以生产模式在后台启动
#
# 注意:
#   * 默认模式为开发模式 (-d)。
#   * 在后台运行时，请使用 'tail -f logs/app.log' 查看日志。

set -euo pipefail

MODE="dev"
BACKGROUND=false

# 参数解析
while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--dev) MODE="dev"; shift ;;
    -p|--prod) MODE="prod"; shift ;;
    -b|--background) BACKGROUND=true; shift ;;
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

# 日志目录
LOG_DIR="logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/server.log"
ERR_FILE="$LOG_DIR/server.err"

# 构建 CMD
CMD=(app.main:app --host "$HOST" --port "$PORT")
if [[ "${DEBUG:-}" == "True" ]]; then
  CMD+=("--reload")
fi

# 判断系统类型
OS_TYPE=$(uname)
if [[ "$OS_TYPE" == "Darwin" ]]; then
    PY_CMD=(python -u -m uvicorn "${CMD[@]}")
else
    # Linux
    PY_CMD=(stdbuf -oL python -m uvicorn "${CMD[@]}")
fi

echo "以 ${MODE} 模式启动服务: ${PY_CMD[*]}"

if $BACKGROUND; then
    echo "服务以后台模式运行，日志: $LOG_FILE"
    nohup "${PY_CMD[@]}" >"$LOG_FILE" 2>"$ERR_FILE" &
else
    # 前台运行 + trap
    trap 'kill -INT $uvicorn_pid' INT TERM
    "${PY_CMD[@]}" 2>&1 | tee "$LOG_FILE" &
    uvicorn_pid=$!
    wait $uvicorn_pid
fi
