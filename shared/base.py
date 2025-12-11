"""Base classes for all projects."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Generic
from enum import Enum
import json
import hashlib

import numpy as np
from pydantic import BaseModel


class ExperimentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExperimentResult:
    """Container for experiment results."""
    
    experiment_id: str
    project_name: str
    status: ExperimentStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "project_name": self.project_name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "parameters": self.parameters,
            "metrics": self.metrics,
            "artifacts": {k: str(v) for k, v in self.artifacts.items()},
            "logs": self.logs,
            "error": self.error,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
    
    @property
    def duration(self) -> Optional[float]:
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None


T = TypeVar('T')


class BaseExperiment(ABC, Generic[T]):
    """Abstract base class for experiments."""
    
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.params = kwargs
        self._result: Optional[ExperimentResult] = None
    
    @abstractmethod
    def setup(self) -> None:
        """Setup experiment resources."""
        pass
    
    @abstractmethod
    def run(self) -> T:
        """Execute the experiment."""
        pass
    
    @abstractmethod
    def teardown(self) -> None:
        """Cleanup resources."""
        pass
    
    def execute(self) -> ExperimentResult:
        """Full experiment lifecycle."""
        exp_id = self._generate_id()
        result = ExperimentResult(
            experiment_id=exp_id,
            project_name=self.name,
            status=ExperimentStatus.PENDING,
            start_time=datetime.now(),
            parameters=self.params,
        )
        
        try:
            result.status = ExperimentStatus.RUNNING
            self.setup()
            output = self.run()
            result.artifacts["output"] = output
            result.status = ExperimentStatus.COMPLETED
        except Exception as e:
            result.status = ExperimentStatus.FAILED
            result.error = str(e)
            raise
        finally:
            result.end_time = datetime.now()
            self.teardown()
            self._result = result
        
        return result
    
    def _generate_id(self) -> str:
        content = f"{self.name}-{self.params}-{datetime.now().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]


class BaseProject(ABC):
    """Abstract base class for all projects."""
    
    PROJECT_NAME: str = "base"
    VERSION: str = "1.0.0"
    
    def __init__(self):
        self.experiments: List[ExperimentResult] = []
        self._initialized = False
    
    @abstractmethod
    def get_description(self) -> str:
        """Return project description."""
        pass
    
    @abstractmethod
    def get_experiments(self) -> List[str]:
        """List available experiments."""
        pass
    
    @abstractmethod
    def run_experiment(self, name: str, **kwargs) -> ExperimentResult:
        """Run a specific experiment."""
        pass
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Return UI configuration for Streamlit."""
        return {
            "name": self.PROJECT_NAME,
            "version": self.VERSION,
            "description": self.get_description(),
            "experiments": self.get_experiments(),
        }


class APIRequest(BaseModel):
    """Base API request model."""
    experiment_name: str
    parameters: Dict[str, Any] = {}


class APIResponse(BaseModel):
    """Base API response model."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None