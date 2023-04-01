from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class Response:
    title: str
    image: str
    
class NasaAPI(ABC):
    @abstractmethod
    async def get_response(self) -> Response:
        raise NotImplementedError()