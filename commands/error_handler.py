from discord.ext.commands import Cog,  command, Context
from .resources import exceptions
from discord import Interaction, app_commands

from bot import Bot
from .resources.exceptions import CustomCheckError
from .resources.AutomatedMessages import AutoEmbed
import json
import traceback
import random
import string
import logging

error_dict = json.load(open("errors.json", "r", encoding="utf-8"))

logger = logging.getLogger("errors")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(
    filename="errors.log", encoding="utf-8", mode="a")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        bot.tree.error(coro = self.dispatch_slash_command_error)

    async def dispatch_slash_command_error(self, interaction: Interaction, error:  app_commands.AppCommandError):
        self.bot.dispatch("app_command_error", interaction, error)

    @Cog.listener('on_app_command_error')
    async def on_slash_command_error(self, inter: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandNotFound):
            return
        
        if isinstance(error, exceptions.NotOwner):
            return await inter.response.send_message(
                embed=AutoEmbed().type_autoembed(
                    type="error",
                    description=f"```Вы не можете использовать данную команду.```"
                ), ephemeral=True
            )
        if isinstance(error, CustomCheckError):
            return await inter.response.send_message(
                embed=AutoEmbed().type_autoembed(
                    type="error",
                    description=f"```{error.message}```"
                ), ephemeral=True
            )


        if error.__class__.__name__ in error_dict:
            if not isinstance(error, app_commands.CommandInvokeError):
                argument = getattr(error, 'argument', None) or getattr(error, 'retry_after', None) or (getattr(error, 'param', None)).name

                description = f"```{error_dict[error.__class__.__name__]}```"
                if argument:
                    description = description.format(argument=argument)

                return await inter.response.send_message(
                    embed=AutoEmbed().type_autoembed(
                        type="error",
                        description=description,
                    ), ephemeral=True
                )

        error_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(9))
        logger.exception(f"\n------------------- {error_id} -------------------\n{''.join(traceback.format_exception(type(error), value=error, tb=error.__traceback__))}")
        
        message = error_dict['UnknownError']

        if isinstance(error,  app_commands.CommandInvokeError):
            message = error_dict['CommandInvokeError']

        await inter.response.send_message(
            embed=AutoEmbed().type_autoembed(
                type="error",
                description=f"```{message}```",
                error_id=error_id,
                dev_link=True
            ), ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
