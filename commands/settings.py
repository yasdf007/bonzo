from discord import message
from discord.ext.commands import (
    Cog,
    CommandError,
    MissingPermissions,
    BucketType,
    MissingRequiredArgument,
    CommandOnCooldown,
    InvalidEndOfQuotedStringError,
    ExpectedClosingQuoteError,
    guild_only,
    command,
    has_permissions,
    cooldown,
)
from discord.ext.commands.context import Context
from commands.resources.AutomatedMessages import automata
from database import db


class PrefixTooLong(CommandError):
    pass


class PrefixTooShort(CommandError):
    pass


class NoSpecialSymbolFound(CommandError):
    pass


class NotASCII(CommandError):
    pass


class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return await ctx.send(embed=automata.generateEmbErr("Ты не администратор"))

        if isinstance(error, PrefixTooLong):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Префикс слишком длинный (макс. 5 символов)"
                )
            )

        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(
                embed=automata.generateEmbErr("Нужно указать префикс")
            )

        if isinstance(error, PrefixTooShort):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Префикс слишком короткий (мин. 1 символ)"
                )
            )

        if isinstance(error, NoSpecialSymbolFound):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Префикс должен заканчиваться спец. символом, доступны [_.,!#$%^&*()<>?/\|}{~:]'"
                )
            )

        if isinstance(
            error, (InvalidEndOfQuotedStringError, ExpectedClosingQuoteError)
        ):
            return await ctx.send(
                embed=automata.generateEmbErr("Двойные кавычки недопустимы")
            )

        if isinstance(error, NotASCII):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Префикс должен состоять только из ascii символов"
                )
            )

        if isinstance(error, CommandOnCooldown):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    f"Нельзя часто менять префикс. Попробуй через {error.retry_after: .0f}с."
                )
            )

        raise error

    @guild_only()
    @cooldown(rate=4, per=120, type=BucketType.guild)
    @has_permissions(administrator=True)
    @command(
        name="set_prefix",
        description="Устанавливает пользовательский префикс для бота (только для админов, макс. 5 символов, без двойных кавечек)",
    )
    async def set_prefix(self, ctx: Context, prefix: str):
        if not ctx.message.guild:
            raise

        if len(prefix) < 1:
            raise PrefixTooShort
        if len(prefix) > 5:
            raise PrefixTooLong

        if not prefix.isascii():
            raise NotASCII

        prefix = rf"{prefix}"

        if prefix[-1] not in "[_.!#$%^&*()<>?/\|}{~:]'":
            raise NoSpecialSymbolFound

        self.bot.custom_prefix[ctx.message.guild.id] = prefix
        await db.insertPrefix(self.bot.pool, ctx.message.guild.id, prefix)
        await ctx.send(f"Установил префикс {prefix} для {ctx.message.guild.name}!")


def setup(bot):
    bot.add_cog(Settings(bot))
