"""Configuration management."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from functools import lru_cache

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    """Application configuration."""
    
    # App settings
    APP_NAME: str = "ML Complexity Research Suite"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CACHE_DIR: Path = BASE_DIR / ".cache"
    RESULTS_DIR: Path = BASE_DIR / "results"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    # Dashboard
    DASHBOARD_HOST: str = "0.0.0.0"
    DASHBOARD_PORT: int = 8501
    
    # Compute
    MAX_WORKERS: int = 4
    BATCH_SIZE: int = 32
    DEFAULT_SEED: int = 42
    
    # Project-specific
    BENCHMARK_ITERATIONS: int = 100
    MAX_PROBLEM_SIZE: int = 10000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_config() -> Config:
    """Get cached configuration instance."""
    config = Config()
    
    # Ensure directories exist
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    return config


@dataclass
class ProjectConfig:
    """Per-project configuration."""
    
    name: str
    enabled: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectConfig":
        return cls(**data)
