from discord.ext.commands import (
    Cog,
    BucketType,
    guild_only,
    has_permissions,
    cooldown,
    hybrid_command,
    Context
)
from dependencies.repository.prefix.abc import PrefixRepository
from bot import Bot
from .resources.exceptions import CustomCheckError

class Settings(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.prefix_repo: PrefixRepository = self.bot.dependency.prefix_repo

    @hybrid_command(
        name="set_prefix",
        description="Устанавливает серверный префикс для бота (только для админов, макс. 5 символов, без двойных кавечек)",
    )
    @guild_only()
    @cooldown(rate=4, per=120, type=BucketType.guild)
    @has_permissions(administrator=True)
    async def set_prefix(self, ctx: Context, prefix: str):
        if not ctx.message.guild:
            raise
        if len(prefix) < 1:
            raise CustomCheckError(message="Префикс слишком короткий (мин. 1 символ)")
        if len(prefix) > 5:
            raise CustomCheckError(message="Префикс слишком длинный (макс. 5 символов)")

        if not prefix.isascii():
            raise CustomCheckError(message="Префикс должен состоять только из ascii символов")

        prefix = rf"{prefix}"

        if prefix[-1] not in "[_.!#$%^&*()<>?/\|}{~:]'":
            raise CustomCheckError(message= "Префикс должен заканчиваться спец. символом, доступны [_.,!#$%^&*()<>?/\|}{~:]'")

        await self.prefix_repo.insertPrefix(guild_id=ctx.message.guild.id, prefix=prefix)
        await ctx.send(f"Установил префикс {prefix} для {ctx.message.guild.name}!")


async def setup(bot):
    await bot.add_cog(Settings(bot))
