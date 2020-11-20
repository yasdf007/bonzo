from discord import Embed
from discord.ext import commands
from discord.member import Member
from random import randint


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'{error.argument} не найден')

    @commands.command()
    async def info(self, ctx, member: Member):
        embed = Embed(
            title=f'Информация о {member.display_name}', color=randint(0, 0xFFFFFF))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Подрубился на сервер',
                        value=member.joined_at.strftime('%d %B %Y %R UTC'), inline=False)
        embed.add_field(name='Появился на свет',
                        value=member.created_at.strftime('%d %B %Y %R UTC'), inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
