#!/bin/bash

# 定义 proto 文件的根目录和生成的 Python 文件的目标目录
PROTO_DIR="protos"
GENERATED_DIR="generated"

# 检查并创建生成目录
mkdir -p "$GENERATED_DIR"

echo "开始编译 .proto 文件..."

# 遍历 protos 目录下的所有子目录
for service_dir in "$PROTO_DIR"/*; do
    if [ -d "$service_dir" ]; then
        service_name=$(basename "$service_dir")

        # 为当前服务创建生成目录
        mkdir -p "$GENERATED_DIR/$service_name"

        echo "正在编译服务: $service_name"

        # 使用 grpcio-tools 编译 proto 文件
        python -m grpc_tools.protoc \
            -I"$PROTO_DIR" \
            --python_out="$GENERATED_DIR" \
            --pyi_out="$GENERATED_DIR" \
            --grpc_python_out="$GENERATED_DIR" \
            "$PROTO_DIR"/*/*.proto

        echo "编译完成：$GENERATED_DIR/$service_name"
    fi
done

echo "所有 .proto 文件编译完毕。"
