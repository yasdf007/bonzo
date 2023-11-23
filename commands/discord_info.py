from discord import Embed, app_commands, Spotify, CustomActivity, Member, Interaction
from discord.ext.commands import Cog
from discord.ext.commands.core import guild_only
from bot import Bot
import os

osname = os.name

class DiscordInfo(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @app_commands.command(name="ping", description='Понг!')
    async def ping(self, inter: Interaction):
        botLatency = round(inter.client.latency * 1000, 2)
        await inter.response.send_message(f"Pong! {str(botLatency)}ms (задержка)")

    # функция, отправляющая информацию о сервере
    @guild_only()
    @app_commands.command(name='serverinfo', description='Показывает информацию о сервере')
    async def serverinfo(self, inter: Interaction):
        server = inter.guild
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
            text=f"/by bonzo/ for {inter.user.name}", icon_url=inter.user.display_avatar.with_format("png")
        )

        await inter.response.send_message(embed=embed)


    @guild_only()
    @app_commands.command(name='info', description='Выдаёт информацию о пользователе')
    async def user_info(self, inter: Interaction, member: Member = None):
        if not member:
            member = inter.user
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

        await inter.response.send_message(embed=embed)

    @app_commands.command(name='status', description='Статус бота на данный момент')
    async def status(self, inter: Interaction):
        embed = Embed(title="**Информация**", color=0x1fcf48)

        embed.set_thumbnail(url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")

        botLatency = round(self.bot.latency * 1000, 2)
        Voice = len(self.bot.voice_clients)
        embed.add_field(name="**Status** <a:signal_ping:925751007592480818>", value=f"**ping: **`{botLatency}ms`\n**os: **`{osname}`\n**in voices: **`{Voice}`")

        emojis = len(self.bot.emojis)
        guilds = len(self.bot.guilds)
        Users  = len(self.bot.users)
        embed.add_field(name="**Сounts **<a:slipp:991673495018807376>", value=f"**users: **`{Users} `\n**guilds: **`{guilds} `\n**emojis: **`{emojis}`")
       
        voice_channels_count = 0
        for guild in self.bot.guilds:
            voice_channels_count += len(guild.voice_channels)
        channels_count = 0
        for guild in self.bot.guilds:
            channels_count += len(guild.channels)
        embed.add_field(name="**Channels count** <a:your_shard:991782924921868418>", value=f"**channels: **`{channels_count}`\n**voices: **`{voice_channels_count}`")


        embed.set_footer(text="/by bonzo/")

        await inter.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DiscordInfo(bot))
