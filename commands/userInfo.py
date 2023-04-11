from discord import Embed, Spotify, CustomActivity
from discord.ext.commands import Cog, hybrid_command, Context
from discord.member import Member
from discord.ext.commands.core import guild_only
from bot import Bot

name = "info"
description = "Выдаёт информацию о пользователе"


class Info(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @hybrid_command(name=name, description=description)
    @guild_only()
    async def info(self, ctx: Context, member: Member = None):
        if not member:
            member = ctx.author
        embed = Embed(
            title=f"Информация о {member.display_name}", color=member.top_role.colour
        )

        embed.set_thumbnail(url=member.display_avatar.with_static_format("png"))

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


async def setup(bot):
    await bot.add_cog(Info(bot))
