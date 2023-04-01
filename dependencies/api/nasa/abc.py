from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class Response:
    title: str
    image: str
    
class NasaAPI(ABC):
    @abstractmethod
    async def get_image_of_the_day(self) -> Response:
        raise NotImplementedError()