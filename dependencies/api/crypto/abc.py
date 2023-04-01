from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Response:
    name: str
    symbol: str
    price_usd: float
    
class CryptoAPI(ABC):
    @abstractmethod
    async def get_biggest_currencies(self) -> List[Response]:
        raise NotImplementedError()