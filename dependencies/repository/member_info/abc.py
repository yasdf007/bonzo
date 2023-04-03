from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class MemberInfo:
    xp: int
    text_xp_at: float
    
@dataclass
class Leaderboard:
    member_id: int
    xp: int

@dataclass
class Rank:
    xp: int
    rank: int
    overall_ranks: int

class MemberHandlerRepository(ABC):
    @abstractmethod
    async def insert_member(self, guild_id: int, member_id: int):
        raise NotImplementedError()
        
    @abstractmethod
    async def remove_member(self, guild_id: int, member_id: int):
        raise NotImplementedError()
    
    @abstractmethod
    async def get_member_info(self, guild_id: int, member_id: int) -> MemberInfo:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_member_info(self, guild_id: int, member_id: int, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def leaderboard(self, guild_id: int) -> List[Leaderboard]:
        raise NotImplementedError()

    @abstractmethod
    async def rank(self, guild_id: int, member_id: int)-> Rank:
        raise NotImplementedError()

