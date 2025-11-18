import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'generated'))

from fastapi import FastAPI
from .core.cors import register_cors
from .core.lifespan import lifespan
from .core.exception_handler import register_exception_handlers
from .routers.http import router as http_router

app = FastAPI(title="FastApi Service", lifespan=lifespan)

# 注册路由
app.include_router(http_router)
# 注册异常处理
register_exception_handlers(app)
# 注册 CORS
register_cors(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Service"}

@app.get("/health")
def read_root():
    return ""
