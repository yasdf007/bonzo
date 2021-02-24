from discord import Embed
from discord.ext.commands import Cog, command

name = 'invite'
description = 'Ссылка на приглашение бота'


class invite(Cog):
    def __init__(self, bot):
        self.bot = bot

    # функция, отправляющая инвайт-ссылку бота в чат
    @command(name=name, description=description)
    async def invite(self, ctx):
        embedd = Embed(
            title='**зовём /bonzo/ на ваш сервер...**', colour=0xb84000)
        embedd.set_thumbnail(
            url='https://i.ibb.co/Xk7qTy4/BOnzo-1.png')
        embedd.add_field(
            name='кликните вот', value='[сюда](https://discordapp.com/api/oauth2/authorize?client_id=680132907859443790&permissions=8&scope=bot)')
        embedd.set_footer(text="/by bonzo/ for @" + ctx.message.author.name)
        await ctx.message.reply(embed=embedd)


def setup(bot):
    bot.add_cog(invite(bot))
