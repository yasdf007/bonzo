from discord import Embed
from discord.ext.commands import Cog, hybrid_command, Context
from discord.ext.commands.core import guild_only
from discord.ext.commands import NoPrivateMessage
from .resources.AutomatedMessages import automata
from bot import Bot


name = "serverinfo"
description = "Показывает информацию о сервере"



class info(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, NoPrivateMessage):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Эту команду нельзя использовать в ЛС.", error=error
                )
            )
        raise error

    # функция, отправляющая информацию о сервере
    @hybrid_command(name=name, description=description)
    @guild_only()
    async def serverinfo(self, ctx: Context):
        server = ctx.guild
        embed = Embed(title="**Информация о сервере:**", colour=0x7D07DE)

        embed.set_thumbnail(url=server.icon.with_format("png") if server.icon else server.icon)

        embed.add_field(name="**Название:**", value=f"{server.name}", inline=False)

        embed.add_field(
            name="**Сервер создан:**",
            value=server.created_at.strftime("%d %B %Y %R UTC"),
            inline=False,
        )

        embed.add_field(
            name="**Количество участников:**",
            value=f"{server.member_count}",
            inline=False,
        )

        embed.add_field(
            name="**Всего текстовых каналов:**",
            value=f"{len(server.text_channels)}",
            inline=False,
        )

        embed.add_field(
            name="**Всего голосовых каналов:**",
            value=f"{len(server.voice_channels)}",
            inline=False,
        )

        embed.add_field(
            name="**Максимальное количество эмодзи:**",
            value=f"{server.emoji_limit} ",
            inline=False,
        )

        embed.add_field(
            name="**Уровень сервера**", value=f"{server.premium_tier}", inline=False
        )

        embed.add_field(
            name="**Бустов сервера**",
            value=f"{server.premium_subscription_count}",
            inline=False,
        )

        embed.set_footer(
            text=f"/by bonzo/ for {ctx.author}", icon_url=ctx.author.display_avatar.with_format("png")
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(info(bot))
