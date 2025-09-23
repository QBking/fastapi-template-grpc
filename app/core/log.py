import sys
from loguru import logger
from .config import settings


def setup_logging():
    """
    配置并设置日志记录器。

    根据环境变量，移除默认的日志处理器，并添加新的处理器。
    """
    # 移除默认的处理器
    logger.remove()

    # 为不同的环境添加不同的日志处理器
    if settings.ENV == "dev":
        # 开发环境：打印到控制台，级别为 DEBUG
        logger.add(
            sys.stderr,
            level="DEBUG",
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
    elif settings.ENV == "prod":
        # 生产环境：日志写入文件，级别为 INFO
        # 每天轮转一个新文件，只保留最近 14 天的日志
        logger.add(
            "logs/app.log",
            level="INFO",
            rotation="00:00",
            retention="14 days",
            compression="zip",
            encoding="utf-8",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
        )
        # 错误日志写入单独的文件
        logger.add(
            "logs/app_error.log",
            level="ERROR",
            rotation="00:00",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
        )
    else:
        # 其他环境，默认打印到控制台
        logger.add(sys.stderr, level="INFO")


# 调用函数来设置日志
setup_logging()

# 导出 logger 实例，方便其他模块直接导入
__all__ = ["logger"]
