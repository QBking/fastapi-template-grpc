from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import demo
from .core.config import settings
from .core.exception_handler import register_exception_handlers

app = FastAPI(title="FastApi Service")

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
