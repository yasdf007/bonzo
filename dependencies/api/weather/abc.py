from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class Response:
    city: str
    weatherType: str
    temp: int
    wind_speed: float
    wind_direction: str
    humidity: float
    weatherCountry: Optional[str] = None
    
class WeatherAPI(ABC):
    @abstractmethod
    async def get_response(self, city: str) -> Response:
        raise NotImplementedError()