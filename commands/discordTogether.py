from discord.ext.commands import Cog, command, bot_has_permissions, Context
from discord.ext.commands.errors import BotMissingPermissions
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.error import SlashCommandError
from discord_slash.utils.manage_commands import create_choice
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from commands.resources.AutomatedMessages import automata

name = "activity"
description = "Создает в канале активити по запросу (по умолчанию - youtube)"


class IncorrectActivity(commands.CommandError, SlashCommandError):
    pass


class NotInVoice(commands.CommandError, SlashCommandError):
    pass


defaultApplications = {
    # Credits to RemyK888
    "youtube": "880218394199220334",
    "poker": "755827207812677713",
    "betrayal": "773336526917861400",
    "fishing": "814288819477020702",
    "chess": "832012774040141894",
    # Credits to awesomehet2124
    "letter-tile": "879863686565621790",
    "word-snack": "879863976006127627",
    "doodle-crew": "878067389634314250",
    # 'spellcast': '852509694341283871',
    # 'awkword': '879863881349087252',
    # 'checkers': '832013003968348200',
}


class YtTogether(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "У bonzo недостаточно прав для исполнения данной команды",
                    error=error,
                )
            )
        if isinstance(error, NotInVoice):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Для использования команды нужно находиться в голосовом канале",
                    error=error,
                )
            )
        if isinstance(error, IncorrectActivity):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    f"Указанной activity не существует\nДоступны {', '.join(defaultApplications.keys())}",
                    error=error,
                )
            )
        raise error

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, NotInVoice):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Для использования команды нужно находиться в голосовом канале",
                    error=error,
                )
            )
        if isinstance(error, IncorrectActivity):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    f"Указанной activity не существует\nДоступны {', '.join(defaultApplications.keys())}",
                    error=error,
                )
            )
        raise error

    @bot_has_permissions(create_instant_invite=True)
    @command(name=name, description=description)
    async def activity_prefix(self, ctx: Context, activity: str = "youtube"):
        if not activity in defaultApplications:
            raise IncorrectActivity

        await self.activity(ctx, activity)

    @cog_ext.cog_slash(
        name=name,
        description=description,
        options=[
            {
                "name": name,
                "description": description,
                "type": 3,
                "required": "true",
                "choices": [
                    create_choice(name=activity, value=activity)
                    for activity in defaultApplications
                ],
            }
        ],
    )
    async def activity_slash(self, ctx: SlashContext, activity: str):
        if not activity in defaultApplications:
            raise IncorrectActivity

        await self.activity(ctx, activity)

    async def activity(self, ctx, activity):
        if not ctx.author.voice:
            raise NotInVoice
        link = await self.bot.togetherControl.create_link(
            ctx.author.voice.channel.id, activity
        )
        buttons = []
        buttons.append(create_button(style=ButtonStyle.URL, label=activity, url=link))

        action_row = create_actionrow(*buttons)
        await ctx.send(f"⬇️  ⬇️\n", components=[action_row])


def setup(bot):
    bot.add_cog(YtTogether(bot))
