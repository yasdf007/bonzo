from discord.channel import DMChannel
from discord.ext.commands import (
    Cog,
    guild_only,
    hybrid_command,
    Context
)
from discord import Embed, File, Asset
from datetime import datetime, timedelta

from .resources.xp_system.abc import XpStrategy
from .resources.xp_system.xp import OriginalXP
from .resources.xp_system.image import ImageGeneration

from dependencies.repository.member_info.abc import MemberHandlerRepository
from dependencies.repository.member_info.memory import MemberHandlerRepositoryMemory
from database.memory.db import DictMemoryDB

from bot import Bot


class AddXP(Cog):
    def __init__(self, bot, xp_strategy: XpStrategy, image_creation: ImageGeneration, members_repo: MemberHandlerRepository):
        self.bot: Bot = bot
        self.xp_strategy = xp_strategy
        self.image_creation = image_creation
        self.members_repo = members_repo

    @Cog.listener()
    async def on_member_join(self, member):
        await self.members_repo.insert_member(member.guild.id, member.id)

    @Cog.listener()
    async def on_member_remove(self, member):
        await self.members_repo.remove_member(member.guild.id, member.id)


    def percentsToLvlUp(self, currentXp, currentLVL):
        xpToGetCurrentLVL = self.xp_strategy.xp_from_level(currentLVL)
        xpToGetNextLVL = self.xp_strategy.xp_from_level(currentLVL + 1)

        devinded = currentXp - xpToGetCurrentLVL
        devider = xpToGetNextLVL - xpToGetCurrentLVL

        return round((devinded / devider) * 100, 2)


    @Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, DMChannel):
            return
        if message.author.bot:
            return

        await self.addMessageXp(message.author)

    async def checkAfter(self, channel):
        # Массив из людей в войсе без ботов
        membersInVoice = list(filter(lambda x: x.bot == False, channel.members))

        # Если больше одного, то для каждого генерим опыт,
        # если уже нет таска для опыта
        if len(membersInVoice) >= 2:

            for member in membersInVoice:
                if self.bot.scheduler.get_job(f"{member.id}") is None:
                    await self.addVoiceJob(member)

    async def checkBefore(self, channel):
        membersInVoice = list(filter(lambda x: x.bot == False, channel.members))

        if len(membersInVoice) == 1:
            for member in membersInVoice:
                self.bot.scheduler.remove_job(f"{member.id}")

    async def checkBeforeAndAfter(self, before, after):
        await self.checkBefore(before)
        await self.checkAfter(after)

    async def checkAfkOrDeaf(self, member):
        job = self.bot.scheduler.get_job(f"{member.id}")

        if job:
            if (
                member.voice.channel.name == member.guild.afk_channel
            ) or member.voice.self_deaf == True:
                self.bot.scheduler.pause_job(f"{member.id}")
            else:
                self.bot.scheduler.resume_job(f"{member.id}")

    # @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        # Заход
        if after.channel and not before.channel:
            await self.checkAfter(after.channel)

        # Выход
        if before.channel and not after.channel:
            if self.bot.scheduler.get_job(f"{member.id}"):
                self.bot.scheduler.remove_job(f"{member.id}")

            await self.checkBefore(before.channel)

        # Перемещение по каналам
        if before.channel and after.channel:
            if before.channel != after.channel:
                if self.bot.scheduler.get_job(f"{member.id}"):
                    self.bot.scheduler.remove_job(f"{member.id}")

                await self.checkBeforeAndAfter(before.channel, after.channel)

        await self.checkAfkOrDeaf(member)

    async def addVoiceJob(self, member):
        self.bot.scheduler.add_job(
            self.addVoiceXp, "interval", minutes=1, id=f"{member.id}", args=[member]
        )

    async def addMessageXp(self, member):
        xpInfo = await self.members_repo.get_member_info(member.guild.id, member.id)

        if datetime.now().timestamp() > xpInfo.text_xp_at:
            newXp = xpInfo.xp + self.xp_strategy.message_xp
            next_text_xp_at = (datetime.now() + timedelta(seconds=60)).timestamp()
            await self.members_repo.update_member_info(member.guild.id, member.id, xp=newXp, text_xp_at=next_text_xp_at)

    async def addVoiceXp(self, member):
        xpInfo = await self.members_repo.get_member_info(member.guild.id, member.id)
        
        xp = xpInfo.xp

        newXp = xp + self.xp_strategy.voice_xp
        await self.members_repo.update_member_info(member.guild.id, member.id, xp=newXp)

    @hybrid_command(name="top", description="Показывает топ 10 по опыту")
    @guild_only()
    async def leaderboard(self, ctx: Context):
        result = await self.members_repo.leaderboard(ctx.guild.id)

        if result is None:
            await ctx.message.reply("Значения не найдены")
            return

        embed = Embed(title="TOP 10 участников по опыту", color=ctx.author.color)

        embed.set_footer(
            text=f"/by bonzo/ for {ctx.author}", icon_url=ctx.author.display_avatar.with_format("png")
        )
        embed.set_thumbnail(url=ctx.guild.icon.with_format("png")) if ctx.guild.icon else None

        for user in result:
            member = ctx.guild.get_member(user.member_id)
            lvl = self.xp_strategy.level_from_xp(user.xp)
            
            if not member:
                embed.add_field(
                    name=f"*Пользователя нет на сервере*",
                    value=f"LVL: {lvl}\nEXP: {user.xp}",
                    inline=False,
                )
                await self.members_repo.remove_member(ctx.guild.id, user.member_id)
            else:
                embed.add_field(
                    name=f"`{member.display_name}`",
                    value=f"LVL: {lvl}\nEXP: {user.xp}",
                    inline=False,
                )

        await ctx.send(embed=embed)


    @hybrid_command(name="rank", description="Показывает персональную карточку с уровнем")
    @guild_only()
    async def rank(self, ctx: Context):
        result = await self.members_repo.rank(ctx.guild.id, ctx.author.id)
        
        photo_bytes = await Asset.read(ctx.author.display_avatar.with_format("png"))
        
        lvl = self.xp_strategy.level_from_xp(result.xp)
        
        percents = self.percentsToLvlUp(result.xp, lvl)

        async with self.image_creation.create_card(ctx.author, result.xp, self.xp_strategy.xp_from_level(lvl+1), lvl, result.rank, photo_bytes, percents, result.overall_ranks) as card:
            await ctx.send(file=File(fp=card, filename="now.png"))


async def setup(bot):
    xp_strategy = OriginalXP()
    image_gen = ImageGeneration()
    member_repo = MemberHandlerRepositoryMemory(DictMemoryDB)
    await bot.add_cog(AddXP(bot, xp_strategy, image_gen, member_repo))
