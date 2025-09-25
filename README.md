# fastapi-template-grpc

`fastapi-template-grpc` 是一个基于 **FastAPI** 框架，集成了 **gRPC** 通信能力的后端服务模板。它旨在提供一个功能完善、结构清晰的微服务开发起点，同时支持传统的 HTTP RESTful API 和高效的 gRPC 协议，可满足前端、后端微服务等多种通信场景。

## 快速开始

### 1\. 克隆项目

```bash
git clone https://github.com/QBking/fastapi-template-grpc.git
cd fastapi-template-grpc
```

### 2\. 环境配置

根据项目根目录下的 `.env.example` 文件，创建 `.env.dev` 和 `.env.prod` 文件，并根据需要配置环境变量。

```bash
# 示例：创建开发环境配置文件
cp .env.example .env.dev
```

### 3\. 安装依赖

本项目同时支持 `uv`（推荐）和 `pip` 安装依赖。

#### 方法一：使用 uv (推荐)

`uv` 是一个高性能的 Python 包管理器，可显著提升依赖安装速度。

```bash
# 安装 uv
pip install uv

# 安装所有依赖
uv sync
```

#### 方法二：使用 pip

```bash
pip install -r requirements.txt
```

### 4\. 编译 Protocol Buffers

在启动服务前，需要将 `.proto` 文件编译成 Python 代码。项目提供了一个便捷的脚本来完成此任务。

```bash
./compile_protos.sh
```

该脚本会编译 `protos` 文件夹下的所有 `.proto` 文件，编译后的文件存放在根目录的 `generated`下

-----

## 项目运行

本项目提供了方便的脚本来管理服务。

### 启动服务

使用 `./start.sh` 脚本来启动服务。

**参数说明**  
- 模式:  
  - `-d, --dev`   开发模式（默认）。使用 `.env.dev`，若 `DEBUG=True` 启用热重载。  
  - `-p, --prod`  生产模式。使用 `.env.prod`。  
- 方式:  
  - `-b, --background`  后台运行，日志输出至 `logs/app.log` 和 `logs/app.err`。  

**示例**  
```bash
./start.sh          # 开发模式前台启动
./start.sh -d -b    # 开发模式后台启动
```

### 停止服务

使用 `./stop.sh` 脚本来关闭在后台运行的服务。

```bash
# 停止开发模式下的服务
./stop.sh -d

# 停止生产模式下的服务
./stop.sh -p
```

-----

## 功能演示

### 1\. HTTP API (FastAPI)

`app/routers/http/demo.py` 包含了多个 HTTP 接口示例，演示了 FastAPI 的路由、Pydantic 请求体验证和依赖注入。

你可以使用任何 HTTP 客户端（如 cURL、Postman 或 Apifox）来测试这些接口。

  * **GET 请求与查询参数验证**
    ```
    # 示例: GET /demo/2?name=John&age=30
    ```
  * **POST 请求与请求体验证**
    ```
    # 示例: POST /demo/3
    # 请求体: {"name": "Jane", "age": 25}
    ```

### 2\. gRPC 服务

  * **gRPC 服务端**:
    `app/routers/grpc/demo.py` 文件实现了 `SayHello` gRPC 接口，它接收一个包含多种数据类型的复杂请求，并返回一个包含嵌套数据的响应。你可以使用 **Apifox** 来进行 gRPC 请求，或者使用下面准备好的接口测试。

  * **gRPC 客户端**:
    `app/routers/http/demo.py` 中的 `/demo/grpc` 接口是一个完美的 gRPC 客户端代码示例。该接口通过 HTTP 触发，但其内部逻辑是向另一个后端 gRPC 服务（由 `.env` 文件配置）发起 gRPC 请求。

    ```python
    # 代码位置: app/routers/http/demo.py
    @router.get("/grpc")
    def demo_grpc():
        """
        这个HTTP接口内部演示了如何作为gRPC客户端调用另一个微服务
        """
        # ... 客户端调用代码
    ```
