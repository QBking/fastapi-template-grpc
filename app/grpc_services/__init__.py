from grpc import server
from .demo_service import DemoService
from generated.demo import demo_service_pb2_grpc
from app.core.log import logger


def register_grpc_services(grpc_server: server):
    """
    集中注册所有 gRPC 服务
    """
    logger.info("注册 gRPC 服务...")

    # 注册 DemoService
    demo_service_pb2_grpc.add_DemoServiceServicer_to_server(DemoService(), grpc_server)

    logger.info("gRPC 服务注册完成。")