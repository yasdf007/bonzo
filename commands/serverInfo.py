from discord import Embed
from discord.ext.commands import Cog, command


name = 'serverinfo'
description = 'Показывает информацию о сервере (BETA)'


class info(Cog):
    def __init__(self, bot):
        self.bot = bot

    # функция, отправляющая информацию о сервере
    @command(name=name, description=description)
    async def serverinfo(self, ctx):
        server = ctx.message.guild

        embed = Embed(
            title='**Информация о сервере:**',
            colour=0x7D07DE
        )

        embed.set_thumbnail(url=server.icon_url)

        embed.add_field(name='**Название:**',
                        value=f'{server.name}', inline=False)

        embed.add_field(name='**Сервак создан:**',
                        value=server.created_at.strftime('%d %B %Y %R UTC'), inline=False)

        embed.add_field(name='**Количество участников:**',
                        value=f'{server.member_count}', inline=False)

        embed.add_field(name='**Всего текстовых каналов:**',
                        value=f'{len(server.text_channels)}', inline=False)

        embed.add_field(name='**Всего голосовых каналов:**',
                        value=f'{len(server.voice_channels)}', inline=False)

        embed.add_field(name='**Максимальное количество эмодзи:**',
                        value=f'{server.emoji_limit} ', inline=False)

        embed.add_field(name='**Уровень сервера**',
                        value=f'{server.premium_tier}', inline=False)

        embed.add_field(name='**Бустов сервера**',
                        value=f'{server.premium_subscription_count}', inline=False)

        embed.set_footer(
            text=f'/by bonzo/ for {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
