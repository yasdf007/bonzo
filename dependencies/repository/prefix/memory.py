from .abc import PrefixRepository
from database.memory.db import DictMemoryDb

class PrefixRepositoryMemory(PrefixRepository):
    scope = 'prefix'

    def __init__(self, db: DictMemoryDb):
        self.db = db

        if self.scope not in self.db.db:
            self.db.db[self.scope] = {}

    async def getAllPrefixes(self):
        return self.db.db[self.scope]

    async def insertPrefix(self, guild_id: int, prefix: str):
        guild_id = str(guild_id)
        self.db.db[self.scope][guild_id] = prefix

    async def prefix_for_guild(self, guild_id: int):
        guild_id = str(guild_id)
        return self.db.db[self.scope].get(guild_id)