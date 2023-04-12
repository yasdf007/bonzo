from discord.ext.commands import Cog,  command, Context
from discord.ext.commands.errors import CommandError, CommandNotFound, NotOwner, CommandInvokeError


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

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, (CommandNotFound, NotOwner)):
            return

        if isinstance(error, CustomCheckError):
            return await ctx.send(
                embed=AutoEmbed().type_autoembed(
                    type="error",
                    description=f"```{error.message}```"
                ),
            )


        if error.__class__.__name__ in error_dict:
            if not isinstance(error, CommandInvokeError):
                argument = getattr(error, 'argument', None) or getattr(error, 'retry_after', None) or (getattr(error, 'param', None)).name

                description = f"```{error_dict[error.__class__.__name__]}```"
                if argument:
                    description = description.format(argument=argument)

                return await ctx.send(
                    embed=AutoEmbed().type_autoembed(
                        type="error",
                        description=description,
                    ),
                )

        error_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(9))
        logger.exception(f"\n------------------- {error_id} -------------------\n{''.join(traceback.format_exception(type(error), value=error, tb=error.__traceback__))}")
        
        message = error_dict['UnknownError']

        if isinstance(error, CommandInvokeError):
            message = error_dict['CommandInvokeError']

        await ctx.send(
            embed=AutoEmbed().type_autoembed(
                type="error",
                description=f"```{message}```",
                error_id=error_id,
                dev_link=True
            ),
        )


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
