from discord.ext.commands import Cog, command, bot_has_permissions, Context
from discord.ext.commands.errors import CommandError, CommandInvokeError, BotMissingPermissions
# from discord_slash import SlashContext, cog_ext
from discord_slash.error import SlashCommandError
from discord_together import DiscordTogether
from commands.resources.AutomatedMessages import automata

name = 'activity'
description = 'Создает в канале активити по запросу (по умолчанию - youtube)'

class IncorrectActivity(CommandError, SlashCommandError):
    pass
class YtTogether(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.defaultApplications = { 
        # Credits to RemyK888
        'youtube': '880218394199220334',
        'poker': '755827207812677713',
        'betrayal': '773336526917861400',
        'fishing': '814288819477020702',
        'chess': '832012774040141894',
            # Credits to awesomehet2124
        'letter-tile': '879863686565621790',
        'word-snack': '879863976006127627',
        'doodle-crew': '878067389634314250'
        }

    async def cog_command_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            return await ctx.send(embed=automata.generateEmbErr('У bonzo недостаточно прав для исполнения данной команды', error=error))
        if isinstance(error, CommandInvokeError):
            return await ctx.send(embed=automata.generateEmbErr('Для использования команды нужно находиться в голосовом канале', error=error))
        if isinstance(error, IncorrectActivity):
            return await ctx.send(embed=automata.generateEmbErr("Указанной activity не существует", error=error))
        raise error

    # @Cog.listener()
    # async def on_slash_command_error(self, ctx, error):
    #     if isinstance(error, BotMissingPermissions):
    #         await ctx.send(f'Не могу создать инвайт (нет прав)')
    #     if isinstance(error, CommandInvokeError):
    #         await ctx.send(f'Надо зайти в войс')

    @command(name=name, description=description)
    async def youtube_prefix(self, ctx: Context, activity: str = 'youtube'):
        if activity in self.defaultApplications:
            await self.start(ctx, activity)
        else:
            raise IncorrectActivity

    # @cog_ext.cog_slash(name=name, description=description)
    # async def youtube_slash(self, ctx: SlashContext):
    #     await self.start(ctx)

    @bot_has_permissions(create_instant_invite=True)
    async def start(self, ctx, activity):
        if not ctx.author.voice.channel.id:
            raise CommandInvokeError

        link = await self.bot.togetherControl.create_link(ctx.author.voice.channel.id, activity)
        await ctx.send(f'Зайти\n{link}')


def setup(bot):
    bot.add_cog(YtTogether(bot))
