from fastapi import HTTPException
from typing import Optional, Any

class AppException(HTTPException):
    def __init__(self, message: str, code: int = 400):
        self.code = code
        self.message = message
        super().__init__(status_code=code, detail=message)


def success(data: Optional[Any] = None, message: str = "success", code: int = 200):
    """
    统一成功响应格式
    """
    return {"code": code, "message": message, "data": data or {}}


def error(message: str = "error", code: int = 400):
    """
    抛出自定义异常，被异常处理器捕获后统一返回
    """
    raise AppException(message, code)
