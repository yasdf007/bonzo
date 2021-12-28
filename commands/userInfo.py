from discord import Embed, Spotify, CustomActivity
from discord.ext.commands import Cog, command, MemberNotFound, CommandError
from discord.ext.commands.context import Context
from discord.member import Member
from discord_slash import SlashContext, cog_ext
from discord.ext.commands.core import guild_only
from config import guilds
from .resources.AutomatedMessages import automata
from discord_slash.error import SlashCommandError
from discord.ext.commands import NoPrivateMessage as NoPrivateMsg

name = "info"
description = "Выдаёт информацию о пользователе"


class NoPrivateMessage(CommandError, SlashCommandError):
    pass


class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            await ctx.message.reply(f"{error.argument} не найден")

        if isinstance(error, (NoPrivateMessage, NoPrivateMsg)):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Эту команду нельзя использовать в ЛС.", error=error
                )
            )

    @Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, NoPrivateMessage):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Эту команду нельзя использовать в ЛС.", error=error
                )
            )

    @guild_only()
    @command(name=name, description=description)
    async def info_prefix(self, ctx: Context, member: Member = None):
        await self.info(ctx, member)

    @cog_ext.cog_slash(name=name, description=description)
    async def info_slash(self, ctx: SlashContext, member: Member = None):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.info(ctx, member)

    async def info(self, ctx, member: Member = None):
        member = member or ctx.author
        embed = Embed(
            title=f"Информация о {member.display_name}", color=member.top_role.colour
        )

        embed.set_thumbnail(url=member.avatar_url_as(static_format="png"))

        embed.add_field(
            name="Учетная запись:",
            value=f"{member.name}#{member.discriminator}",
            inline=False,
        )

        embed.add_field(name="ID:", value=member.id, inline=False)

        # получаем все роли юзера
        allRoles = ", ".join(
            [i.name for i in member.roles[1::] if len(member.roles) > 1]
        )
        if allRoles:
            embed.add_field(name="Роли:", value=f"{allRoles}", inline=False)

        if member.activities:
            for usrActivity in member.activities:

                if isinstance(usrActivity, Spotify):

                    embed.set_thumbnail(url=usrActivity.album_cover_url)
                    embed.color = usrActivity.color

                    trackArtists = ", ".join(usrActivity.artists)

                    embed.set_field_at(
                        index=3 or 4,
                        name="Статус:",
                        value=f"`{usrActivity.type.name} {usrActivity.name}`",
                        inline=False,
                    )

                    embed.add_field(
                        name="Автор:", value=f"`{trackArtists}`", inline=True
                    )
                    embed.add_field(
                        name="Название:", value=f"`{usrActivity.title}`", inline=True
                    )
                    embed.add_field(
                        name="Альбом:", value=f"`{usrActivity.album}`", inline=True
                    )

                elif isinstance(usrActivity, CustomActivity):
                    embed.add_field(
                        name="Статус:",
                        value=f"`{usrActivity.type.name} {usrActivity.name}`",
                        inline=False,
                    )

        embed.add_field(
            name="Цвет ника:",
            value=f"HEX: {member.color} \n \
                                        RGB: {member.color.to_rgb()}",
            inline=False,
        )

        embed.add_field(
            name="Подрубился на сервер:",
            # когда зашел на сервер # %d - день месяца # ---- # %B - полное название месяца #
            # # %Y - год # ---- # %R - время в 24-часовом формате #
            value=member.joined_at.strftime("%d %B %Y %R UTC"),
            inline=False,
        )

        embed.add_field(
            name="Появился на свет:",
            value=member.created_at.strftime("%d %B %Y %R UTC"),
            inline=False,
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
