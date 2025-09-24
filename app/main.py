import sys
import os
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'generated'))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.log import logger
from .core.config import settings
from .core.exception_handler import register_exception_handlers
from .core.grpc_server import start_grpc_server
from .routers import demo


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 服务启动
    logger.info("FastAPI 服务启动中...")
    # 在独立线程中启动 gRPC 服务
    grpc_thread = threading.Thread(target=start_grpc_server)
    grpc_thread.daemon = True
    grpc_thread.start()
    yield
    # 服务停止
    logger.info("FastAPI 服务停止中...")

app = FastAPI(title="FastApi Service", lifespan=lifespan)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(demo.router)
# 注册异常处理
register_exception_handlers(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Service"}
