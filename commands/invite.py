from discord import Embed
from discord.ext.commands import Cog
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'invite'
description = 'Ссылка на приглашение бота'
invlink = 'https://discord.com/api/oauth2/authorize?client_id=680132907859443790&permissions=8&scope=bot%20applications.commands'


class invite(Cog):
    def __init__(self, bot):
        self.bot = bot

    # функция, отправляющая инвайт-ссылку бота в чат
    @cog_ext.cog_slash(name=name, description=description)
    async def invite(self, ctx: SlashContext):
        embedd = Embed(
            title='**зовём /bonzo/ на ваш сервер...**', colour=0xb84000)
        embedd.set_thumbnail(
            url='https://i.ibb.co/Xk7qTy4/BOnzo-1.png')
        embedd.add_field(
            name='кликните вот', value=f'[сюда]({invlink})')
        embedd.set_footer(text="/by bonzo/ for @" + ctx.author.name)
        await ctx.send(embed=embedd)


def setup(bot):
    bot.add_cog(invite(bot))
