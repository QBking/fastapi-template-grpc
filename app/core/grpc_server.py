from concurrent import futures
import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from ..routers.grpc import register_grpc_services
from .config import settings
from .log import logger


def start_grpc_server():
    """
    启动并运行 gRPC 服务
    """
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 注册所有 gRPC 服务
    register_grpc_services(grpc_server)

    # 注册健康检查服务
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, grpc_server)
    # 设置某个服务名为健康，"" 表示整个 gRPC 服务
    health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)

    grpc_address = f"{settings.GRPC_SERVER_HOST}:{settings.GRPC_SERVER_PORT}"
    grpc_server.add_insecure_port(grpc_address)

    logger.info(f"gRPC 服务正在监听：{grpc_address}")
    grpc_server.start()
    grpc_server.wait_for_termination()
