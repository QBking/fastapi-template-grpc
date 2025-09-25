from app.core.log import logger
from generated.demo import demo_service_pb2_grpc, demo_messages_pb2, demo_types_pb2


class DemoService(demo_service_pb2_grpc.DemoServiceServicer):
    """
    DemoService 的 gRPC 服务实现
    """

    def SayHello(self, request, context):
        logger.info(f"gRPC请求：SayHello")

        # 演示如何访问不同类型的请求数据
        logger.info(f"接收到的请求数据:")
        logger.info(f"  greeting: {request.greeting}")
        logger.info(f"  user_id: {request.user_id}")
        logger.info(f"  is_active: {request.is_active}")
        logger.info(f"  score: {request.score}")
        logger.info(f"  sex: {demo_types_pb2.Sex.Name(request.sex)}")
        logger.info(f"  hobbies: {list(request.hobbies)}")
        logger.info(f"  properties: {dict(request.properties)}")
        logger.info(f"  user: id={request.user.id}, name={request.user.name}, age={request.user.age}")

        # 构造一个包含多种类型的响应
        reply_message = f"你好，{request.user.name}！我收到了你的请求。"

        # 构造嵌套的 UserInfo 消息
        returned_user_info = demo_types_pb2.UserInfo(
            id=request.user.id,
            name=request.user.name
        )
        # 设置 UserInfo 的 age 属性
        returned_user_info.age = request.user.age

        return demo_messages_pb2.HelloReply(
            message=reply_message,
            code=200,
            log_messages=["请求处理成功", "数据已回传"],
            returned_user=returned_user_info
        )
