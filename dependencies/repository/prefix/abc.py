from abc import ABC, abstractmethod

class PrefixRepository(ABC):
    db = None
    @abstractmethod
    async def getAllPrefixes(self):
        raise NotImplementedError()

    @abstractmethod
    async def insertPrefix(self, guild_id: int, prefix: str):
        raise NotImplementedError()

    @abstractmethod
    async def prefix_for_guild(self, guild_id: int):
        raise NotImplementedError()