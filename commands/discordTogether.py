from discord.ext.commands import Cog, command, bot_has_permissions
from discord.ext.commands.errors import CommandInvokeError, BotMissingPermissions
from discord_together import DiscordTogether

name = 'youtube'
description = 'Создает канал для совместного просмотра видео'


class YtTogether(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.togetherControl = DiscordTogether(bot)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            await ctx.send(f'Не могу создать инвайт (нет прав)')
        if isinstance(error, CommandInvokeError):
            await ctx.send(f'Надо зайти в войс')

    @bot_has_permissions(create_instant_invite=True)
    @command(name=name, description=description)
    async def start(self, ctx):
        if not ctx.author.voice.channel.id:
            raise CommandInvokeError

        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, '755600276941176913')
        await ctx.send(f'Зайти\n{link}')


def setup(bot):
    bot.add_cog(YtTogether(bot))
