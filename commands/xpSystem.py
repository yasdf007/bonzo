from discord.channel import DMChannel
from discord.ext.commands import (
    Cog,
    command,
    CommandOnCooldown,
    cooldown,
    BucketType,
    guild_only,
    CommandError,
    hybrid_command
)
from discord.ext.commands import NoPrivateMessage as NoPrivateMsg
from discord.ext.commands.context import Context
from discord import Embed, File, Asset
from datetime import datetime, timedelta
from .resources.AutomatedMessages import automata

from .resources.xp_system.abc import XpStrategy
from .resources.xp_system.xp import OriginalXP
from .resources.xp_system.image import ImageGeneration

from dependencies.repository.member_info.abc import MemberHandlerRepository



class NoPrivateMessage(CommandError):
    pass


class AddXP(Cog):
    def __init__(self, bot, xp_strategy: XpStrategy, image_creation: ImageGeneration):
        self.bot = bot
        self.xp_strategy = xp_strategy
        self.members_repo: MemberHandlerRepository = self.bot.dependency.members_repo
        self.image_creation = image_creation

    async def cog_command_error(self, ctx, error):
        raise error
        if isinstance(error, CommandOnCooldown):
            return await ctx.message.reply(error)

        if isinstance(error, (NoPrivateMessage, NoPrivateMsg)):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Эту команду нельзя использовать в ЛС.", error=error
                )
            )

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

    @guild_only()
    @hybrid_command(name="top", description="Показывает топ 10 по опыту")
    async def leaderboard(self, ctx):
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
            else:
                embed.add_field(
                    name=f"`{member.display_name}`",
                    value=f"LVL: {lvl}\nEXP: {user.xp}",
                    inline=False,
                )

        await ctx.send(embed=embed)


    @guild_only()
    @hybrid_command(name="rank", description="Показывает персональную карточку с уровнем")
    async def rank(self, ctx):
        result = await self.members_repo.rank(ctx.guild.id, ctx.author.id)
        
        photo_bytes = await Asset.read(ctx.author.display_avatar.with_format("png"))
        
        lvl = self.xp_strategy.level_from_xp(result.xp)
        
        percents = self.percentsToLvlUp(result.xp, lvl)

        async with self.image_creation.create_card(ctx.author, result.xp, self.xp_strategy.xp_from_level(lvl+1), lvl, result.rank, photo_bytes, percents, result.overall_ranks) as card:
            await ctx.send(file=File(fp=card, filename="now.png"))


async def setup(bot):
    xp_strategy = OriginalXP()
    image_gen = ImageGeneration()
    await bot.add_cog(AddXP(bot, xp_strategy, image_gen))
