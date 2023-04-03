from .abc import MemberHandlerRepository, MemberInfo, Leaderboard, Rank
from database.memory.db import DictMemoryDb 
from datetime import datetime
from dataclasses import replace

class MemberHandlerRepositoryMemory(MemberHandlerRepository):
    scope = 'members'

    def __init__(self, db: DictMemoryDb):
        self.db = db
        if self.scope not in self.db.db:
            self.db.db[self.scope] = {}
        else:
            for guild in self.db.db[self.scope]:
                for member in self.db.db[self.scope][guild]:
                    self.db.db[self.scope][guild][member] = MemberInfo(**self.db.db[self.scope][guild][member])

    async def insert_member(self, guild_id: int, member_id: int):
        guild_id  = str(guild_id)
        member_id  = str(member_id)
        
        if guild_id not in self.db.db[self.scope]:
            self.db.db[self.scope][guild_id] = {}

        self.db.db[self.scope][guild_id][member_id] = MemberInfo(xp=0, text_xp_at=datetime.now().timestamp())

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

    async def update_member_info(self, guild_id: int, member_id: int, **kwargs):
        guild_id  = str(guild_id)
        member_id  = str(member_id)

        if guild_id not in self.db.db[self.scope]:
            self.db.db[self.scope][guild_id] = {}

        if not member_id in self.db.db[self.scope][guild_id]:
            await self.insert_member(guild_id, member_id)
        
        self.db.db[self.scope][guild_id][member_id] = replace(self.db.db[self.scope][guild_id][member_id], **kwargs)

    async def leaderboard(self, guild_id: int):
        guild_id  = str(guild_id)

        return [Leaderboard(int(member_id), member_info.xp) for member_id, member_info in \
            sorted(self.db.db[self.scope][guild_id].items(), key=lambda x: x[1].xp, reverse=True)][:10]

    async def rank(self, guild_id: int, member_id: int):
        guild_id  = str(guild_id)
        member_id  = str(member_id)

        sorted_all = sorted(self.db.db[self.scope][guild_id].items(), key=lambda x: x[1].xp)
        overall_ranks = len(sorted_all)

        for rank, (user_id, member_info)  in enumerate(sorted_all, start=1):
            if user_id == member_id:
                print(Rank(member_info.xp, rank, overall_ranks))

                return Rank(member_info.xp, rank, overall_ranks)
