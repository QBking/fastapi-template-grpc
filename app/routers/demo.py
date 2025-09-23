from typing import List, Optional
from fastapi import APIRouter, Depends
from app.core.response import success, error, AppException
from app.schemas.response import Response
from app.schemas.demo import User, Demo4Params, UserOut

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/")
def home():
    return success(message="欢迎访问demo！")


@router.get("/1")
def demo1():
    if True:
        # raise error("预期报错可以这样返回")  # 支持无状态码
        raise error("预期报错可以这样返回", 409)
    return success()

'''
get请求参数验证，若请求参数不对则自动返回，默认状态码：422

请求示例：http://127.0.0.1:8000/demo/2?name=John
完整请求示例：http://127.0.0.1:8000/demo/2?name=Jane&age=35&sex=true&zip_code=90210
'''
@router.get("/2")
def demo2(data: User = Depends()):
    return success(data=data)


"""
post请求参数验证，参数格式同上

表单示例：
{
    "name": "wang"
}
"""
@router.post("/3")
def demo3(data: User):
    return success(data=data)


"""
嵌套传参示例，见 schemas/demo.Demo4Params 的写法

请求表单示例：
{
    "user": {
        "name": "wang"
    }
}
"""
@router.post("/4")
def demo4(data: Demo4Params):
    return success(data=data)


"""
指定返回格式，用于规范接口，不用也行，因为挺麻烦的（适用于数据库中对表的增删改查）
返回时用 .model_validate() 方法包裹
"""
@router.get("/5", response_model=Response[UserOut])
def demo5(data: User = Depends()):
    return success(UserOut.model_validate(data))
