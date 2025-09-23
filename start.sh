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

# 默认运行模式和运行方式
MODE="dev"
RUN_MODE=""

# 处理命令行参数
for arg in "$@"
do
    case $arg in
        -d|--dev)
        MODE="dev"
        shift
        ;;
        -p|--prod)
        MODE="prod"
        shift
        ;;
        -b|--background)
        RUN_MODE="&"
        shift
        ;;
        *)
        echo "未知的参数: $arg"
        exit 1
        ;;
    esac
done

# 检查环境变量文件是否存在
ENV_FILE=".env.${MODE}"
if [ ! -f "$ENV_FILE" ]; then
    echo "错误: 环境变量文件 $ENV_FILE 不存在。"
    exit 1
fi

# 核心改动在这里：
# 1. 导出 ENV 环境变量，让 Python 代码中也能读取到
export ENV="$MODE"
# 2. 启用自动导出，并加载 .env 文件，这将使所有键值对变为环境变量
set -a
source "$ENV_FILE"
set +a

# 打印即将执行的命令
if [ "$RUN_MODE" = "&" ]; then
    echo "以 ${MODE} 模式在后台启动服务..."
else
    echo "以 ${MODE} 模式在前台启动服务..."
fi

# 定义日志文件路径
LOG_DIR="logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/app.log"
ERR_FILE="$LOG_DIR/app.err"

# 构建 Uvicorn 命令的基本部分
COMMAND="python -m uvicorn app.main:app --host $HOST --port $PORT"

# 根据 DEBUG 变量的值来有条件地添加 --reload 参数
if [ "$DEBUG" = "True" ]; then
    COMMAND="$COMMAND --reload"
fi

echo $COMMAND
# 执行命令并处理输出
if [ "$RUN_MODE" = "&" ]; then
    # 后台运行
    eval $COMMAND > "$LOG_FILE" 2> "$ERR_FILE" $RUN_MODE
    echo "服务已在后台启动。日志文件: $LOG_FILE"
    echo "请使用 'tail -f $LOG_FILE' 查看日志。"
else
    # 前台运行
    eval $COMMAND 2>&1 | tee "$LOG_FILE"
fi