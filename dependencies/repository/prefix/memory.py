from .abc import PrefixRepository

class PrefixRepositoryMemory(PrefixRepository):
    db = {}

    async def getAllPrefixes(self):
        return self.db

    async def insertPrefix(self, guild_id: int, prefix: str):
        self.db[guild_id] = prefix

    async def prefix_for_guild(self, guild_id: int):
        return self.db.get(guild_id)