"""Logging configuration using loguru."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from halo_mcp_server.config import settings

# Remove default handler
logger.remove()


def setup_logger(log_level: Optional[str] = None) -> None:
    """
    Setup logger with configured level and format.

    Args:
        log_level: Override log level from settings
    """
    level = log_level or settings.mcp_log_level

    # Console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>",
        level=level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # File handler for errors
    log_dir = Path.home() / ".halo-mcp-server" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_dir / "halo_mcp_server.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="INFO",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        encoding="utf-8",
    )

    logger.add(
        log_dir / "error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )

    logger.info(f"Logger initialized with level: {level}")
    logger.info(f"Log directory: {log_dir}")


def get_logger(name: str):
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logger.bind(name=name)


# Initialize logger on module import
setup_logger()
