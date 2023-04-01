from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class Response:
    url: str
    
class DvachAPI(ABC):
    @abstractmethod
    async def get_random_url(self) -> Response:
        raise NotImplementedError()