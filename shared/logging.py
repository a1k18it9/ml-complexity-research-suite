"""Logging configuration."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[Path] = None,
) -> None:
    """Configure application logging."""
    level = level or "INFO"
    
    # Remove default handler
    logger.remove()
    
    # Console handler with rich formatting
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )
    
    # File handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} - {message}",
            rotation="10 MB",
            retention="7 days",
            compression="zip",
        )


def get_logger(name: str):
    """Get a named logger instance."""
    return logger.bind(name=name)
