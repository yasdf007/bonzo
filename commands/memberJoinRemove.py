from discord.ext.commands import Cog
from database import db
from dependencies.repository.member_info.abc import MemberHandlerRepository

class memberJoinRemove(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.members_repo: MemberHandlerRepository = self.bot.dependency.members_repo

    @Cog.listener()
    async def on_member_join(self, member):
        await self.members_repo.insert_member(member.guild.id, member.id)

    @Cog.listener()
    async def on_member_remove(self, member):
        await self.members_repo.remove_member(member.guild.id, member.id)


async def setup(bot):
    await bot.add_cog(memberJoinRemove(bot))
