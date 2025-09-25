import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .log import logger
from .grpc_server import start_grpc_server

grpc_thread = None


def on_startup(app: FastAPI):
    """服务启动时执行的逻辑"""
    global grpc_thread
    logger.info("服务启动中...")

    # 启动 gRPC 服务线程
    grpc_thread = threading.Thread(target=start_grpc_server)
    grpc_thread.daemon = True
    grpc_thread.start()

    # TODO: 初始化数据库连接、Redis 等资源
    logger.info("所有资源初始化完成")


def on_shutdown(app: FastAPI):
    """服务关闭时执行的逻辑"""
    logger.info("服务停止中...")
    # TODO: 关闭数据库连接、Redis 连接、定时任务
    logger.info("资源已释放")


@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup(app)
    yield
    on_shutdown(app)