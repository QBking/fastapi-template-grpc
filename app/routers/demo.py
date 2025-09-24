import grpc
from fastapi import APIRouter, Depends
from google.protobuf.json_format import MessageToDict

from app.core.config import settings
from app.core.response import success, error
from app.core.log import logger
from app.schemas.response import Response
from app.schemas.demo import User, Demo4Params, UserOut
from generated.demo_service import demo_pb2_grpc, demo_pb2

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/")
def home():
    return success(message="欢迎访问demo！")


@router.get("/1")
def demo1():
    if True:
        logger.error("预期报错测试日志")
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


@router.get("/grpc")
def demo_grpc():
    local_service_address = settings.LOCAL_SERVICE_GRPC_ADDRESS
    request = demo_pb2.HelloRequest(
        greeting="hello",
        user_id=1622210536,
        is_active=False,
        score=6,
        sex=demo_pb2.Sex.FEMALE,
        hobbies=["ut", "aa", "bb"],
        properties={"bas123": "in est"},
        user=demo_pb2.UserInfo(
            id="dHls8Nu5D_ckHzjNM",
            name="瓦利",
            age=123
        )
    )

    with grpc.insecure_channel(local_service_address) as channel:
        stub = demo_pb2_grpc.DemoServiceStub(channel)
        response = stub.SayHello(request)
        logger.info(f"gRPC 服务返回：{response}")

    json_data = MessageToDict(response, preserving_proto_field_name=True)
    return success(json_data)
