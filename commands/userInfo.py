from discord import Embed
from discord.ext import commands
from discord.member import Member
from random import randint

name = 'info'
description = 'Выдаёт информацию по пользователю'


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'{error.argument} не найден')

    @commands.command(name=name, description=description, aliases=['userinfo'])
    async def info(self, ctx, member: Member):
        embed = Embed(
            title=f'Информация о {member.display_name}', color=member.color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Учетная запись:',
                        value=f'{member.name}#{member.discriminator}', inline=False)
        embed.add_field(name='ID:', value=member.id, inline=False)

        if ctx.message.guild.id == 664485208745050112:

            party = await self.getPartyRoleId((member.roles))

            if party:
                embed.add_field(name='Партия:', value=f'{party}')
            else:
                embed.add_field(
                    name='Партия:', value='Беспартийный :negative_squared_cross_mark:')

        embed.add_field(
            name='Цвет ника:', value=f'HEX: {member.color} \n RGB: {member.color.to_rgb()}', inline=False)
        embed.add_field(name='Подрубился на сервер:',
                        # когда зашел на сервер # %d - день месяца # ---- # %B - полное название месяца #
                        # # %Y - год # ---- # %R - время в 24-часовом формате #
                        value=member.joined_at.strftime('%d %B %Y %R UTC'), inline=False)
        embed.add_field(name='Появился на свет:',
                        value=member.created_at.strftime('%d %B %Y %R UTC'), inline=False)

        await ctx.send(embed=embed)

    async def getPartyRoleId(self, listOfRoles):
        for element in listOfRoles:
            if element.name == 'ANTINOHAME (Партия)':
                return f'{element.name} :white_check_mark:'
            if element.name == 'АУЕ ПУДЖ (Партия)':
                return f'{element.name} :white_check_mark:'


def setup(bot):
    bot.add_cog(Info(bot))
