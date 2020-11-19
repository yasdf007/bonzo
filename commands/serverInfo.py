import discord
from discord.ext import commands


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # функция, отправляющая информацию о сервере
    @commands.command()
    async def serverinfo(self, ctx):
        server = ctx.message.guild
        embed = discord.Embed(
            title='**Информация о сервере:**',
            colour=0x7D07DE
        )
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name='**Название:**',
                        value=str(server.name), inline=False)
        embed.add_field(name='**Количество участников:**',
                        value=str(server.member_count), inline=False)
        embed.set_footer(text='/by bonzo/ for @' + ctx.message.author.name)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))