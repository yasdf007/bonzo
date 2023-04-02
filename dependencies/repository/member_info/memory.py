from .abc import MemberHandlerRepository, MemberInfo
from database.memory.db import DictMemoryDb 
from datetime import datetime

class MemberHandlerRepositoryMemory(MemberHandlerRepository):
    scope = 'members'

    def __init__(self, db: DictMemoryDb):
        self.db = db
        
        if self.scope not in self.db.db:
            self.db.db[self.scope] = {}

    async def insert_member(self, guild_id: int, member_id: int):
        guild_id  = str(guild_id)
        member_id  = str(member_id)
        
        if guild_id not in self.db.db[self.scope]:
            self.db.db[self.scope][guild_id] = {}

        self.db.db[self.scope][guild_id][member_id] = MemberInfo(xp=0, text_xp_at=datetime.now())

    async def remove_member(self, guild_id: int, member_id: int):
        guild_id  = str(guild_id)
        member_id  = str(member_id)

        if guild_id not in self.db.db[self.scope]:
            self.db.db[self.scope][guild_id] = {}

        if member_id in self.db.db[self.scope][guild_id]:

            del self.db.db[self.scope][guild_id][member_id]
    
    async def get_member_info(self, guild_id: int, member_id: int):
        guild_id  = str(guild_id)
        member_id  = str(member_id)

        if guild_id not in self.db.db[self.scope]:
            self.db.db[self.scope][guild_id] = {}

        if not member_id in self.db.db[self.scope][guild_id]:
            await self.insert_member(guild_id, member_id)

        return self.db.db[self.scope][guild_id][member_id]

