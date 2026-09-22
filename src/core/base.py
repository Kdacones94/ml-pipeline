from abc import ABC, abstractmethod
from typing import Any, Dict

class BasePipelineStep(ABC):
    """Abstract Base Class for all executable pipeline steps."""
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass

class BaseDataLoader(ABC):
    """Abstract Base Class for data extraction step."""
    
    @abstractmethod
    def load_observations(self, patient_id: int) -> list:
        pass

class BaseFeatureBuilder(ABC):
    """Abstract Base Class for feature transformation steps."""
    
    @abstractmethod
    def build_features(self, raw_data: Any) -> Any:
        pass
