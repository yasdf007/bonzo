import discord
from discord import Embed
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord_slash import SlashContext, cog_ext

name = 'init'
description = 'Краткая информация об использовании бота / How to start?'
supportserver='https://discord.gg/XDZWus5'

class Inita(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def inita_prefix(self, ctx: Context):
        await self.inita(ctx)

    @cog_ext.cog_slash(name=name, description=description)
    async def invite_slash(self, ctx: SlashContext):
        await self.inita(ctx)
    
    async def inita(self, ctx):
        embed = Embed(
        title='**Начало работы с bonzo**',
        color=discord.Color.random()
        )

        embed.set_thumbnail(url='https://i.ibb.co/Xk7qTy4/BOnzo-1.png')

        embed.add_field(name='**Для использования legacy-команд:**', value='b/help')
        embed.add_field(name='**Для использования slash-команд:**', value='/help')
        embed.add_field(name='**Для связи с разработчиками:**', 
            value=f'[Перейдите на сервер (нажмите сюда)]({supportserver})')

        embed.set_footer(text='/by bonzo/ for everyone :)')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Inita(bot))