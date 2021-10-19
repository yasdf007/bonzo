from discord.ext.commands import Cog, command, bot_has_permissions, Context
from discord.ext.commands.errors import CommandInvokeError, BotMissingPermissions
# from discord_slash import SlashContext, cog_ext
from discord_together import DiscordTogether

name = 'youtube'
description = 'Создает канал для совместного просмотра видео'


class YtTogether(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            await ctx.send(f'Не могу создать инвайт (нет прав)')
        if isinstance(error, CommandInvokeError):
            await ctx.send(f'Надо зайти в войс')

    # @Cog.listener()
    # async def on_slash_command_error(self, ctx, error):
    #     if isinstance(error, BotMissingPermissions):
    #         await ctx.send(f'Не могу создать инвайт (нет прав)')
    #     if isinstance(error, CommandInvokeError):
    #         await ctx.send(f'Надо зайти в войс')

    @command(name=name, description=description)
    async def youtube_prefix(self, ctx: Context):
        await self.start(ctx)

    # @cog_ext.cog_slash(name=name, description=description)
    # async def youtube_slash(self, ctx: SlashContext):
    #     await self.start(ctx)

    @bot_has_permissions(create_instant_invite=True)
    async def start(self, ctx):
        if not ctx.author.voice.channel.id:
            raise CommandInvokeError

        link = await self.bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f'Зайти\n{link}')


def setup(bot):
    bot.add_cog(YtTogether(bot))
