from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.log import logger
from .core.config import settings
from .core.exception_handler import register_exception_handlers
from .routers import demo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 服务启动
    logger.info("FastAPI 服务启动中...")
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
