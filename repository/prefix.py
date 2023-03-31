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

# class PrefixRepositoryPostgres(PrefixRepository):
#     def __init__(self, pool):
#         self.db = pool

class PrefixRepositoryMemory(PrefixRepository):
    db = {707576013449592848: 't/'}

    async def getAllPrefixes(self):
        return self.db

    async def insertPrefix(self, guild_id: int, prefix: str):
        self.db[guild_id] = prefix

    async def prefix_for_guild(self, guild_id: int):
        return self.db[guild_id]