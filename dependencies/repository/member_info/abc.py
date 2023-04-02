from abc import ABC, abstractmethod
from database.models import MemberInfo

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
