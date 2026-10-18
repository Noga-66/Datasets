import logging
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """كل Agent: input/output ثابت، ومش بيعرف حاجة عن Kafka (علشان يتختبر لوحده)."""
    name: str = "agent"

    def __init__(self) -> None:
        self.log = logging.getLogger(f"agent.{self.name}")

    @abstractmethod
    def run(self, *args, **kwargs): ...
