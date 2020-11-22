from discord import Embed
from discord.ext import commands
from discord.member import Member
from random import randint

name='info'
description='Выдаёт информацию по пользователю'

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'{error.argument} не найден')

    @commands.command(name=name, description=description, aliases=['userinfo'])
    async def info(self, ctx, member: Member):
        embed = Embed(
            title=f'Информация о {member.display_name}', color=randint(0, 0xFFFFFF))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Учетная запись:', value=f'{member.name}#{member.discriminator}', inline=False)
        embed.add_field(name='ID:', value=member.id, inline=False)
        embed.add_field(name='Подрубился на сервер:',
                        # когда зашел на сервер # %d - день месяца # ---- # %B - полное название месяца #
                        # # %Y - год # ---- # %R - время в 24-часовом формате #
                        value=member.joined_at.strftime('%d %B %Y %R UTC'), inline=False)
        embed.add_field(name='Появился на свет:',
                        value=member.created_at.strftime('%d %B %Y %R UTC'), inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
