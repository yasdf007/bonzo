from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class Response:
    name: str
    price_before: str
    due_date: str
    game_photo_url: str
    link_to_game: str

class FreeGamesAPI(ABC):
    @abstractmethod
    async def get_free_games(self) -> List[Response]:
        raise NotImplementedError()