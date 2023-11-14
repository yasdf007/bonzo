from .abc import FreeGamesRepository
from database.memory.db import DictMemoryDb

class FreeGamesRepositoryMemory(FreeGamesRepository):
    scope = 'free_games'

    def __init__(self, db: DictMemoryDb):
        self.db = db    

        if self.scope not in self.db.db:
            self.db.db[self.scope] = {}

    async def get_channel_by_guild(self, guild_id: int):
        guild_id = str(guild_id)
        
        ch_id = self.db.db[self.scope].get(guild_id)
        
        if ch_id:
            return int(ch_id)

        return None

    async def get_channels(self):
        return list(map(lambda ch: int(ch), self.db.db[self.scope].values()))

    async def insert_channel(self, guild_id: int, channel_id: int):
        guild_id = str(guild_id)
        channel_id = str(channel_id)
        self.db.db[self.scope][guild_id] = channel_id

    async def delete_channel(self, guild_id: int):
        guild_id = str(guild_id)
        if guild_id in self.db.db[self.scope]:
            del self.db.db[self.scope][guild_id]