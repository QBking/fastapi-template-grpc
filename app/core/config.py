from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Literal, Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'.env.{Literal["dev", "prod"]}',
        env_file_encoding='utf-8'
    )

    ENV: str = "dev"
    CORS_ORIGINS: List[str] = []

    # gRPC 服务配置
    GRPC_SERVER_HOST: str = "0.0.0.0"
    GRPC_SERVER_PORT: int = 50051

    # 后端其他微服务的 gRPC 地址
    LOCAL_SERVICE_GRPC_ADDRESS: Optional[str] = None
    OTHER_SERVICE_GRPC_ADDRESS: Optional[str] = None

settings = Settings()
