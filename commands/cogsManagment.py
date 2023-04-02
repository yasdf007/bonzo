from discord.ext.commands import Cog, command, is_owner, hybrid_command
from discord.ext.commands.errors import MissingPermissions, NotOwner
import traceback

class CogsManagment(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (MissingPermissions, NotOwner)):
            pass
        raise error

    @is_owner()
    @hybrid_command(name="load", description="Загружает ког")
    async def load_cog(self, ctx, cog: str):
        try:
            await self.bot.load_extension("commands." + cog)
        except Exception as e:
            return await ctx.send(f"Невозможно загрузить ког: {traceback.format_exc()}")

        await ctx.send(f"Ког {cog} загружен")

    @is_owner()
    @hybrid_command(name="unload", description="Выгружает ког")
    async def unload_cog(self, ctx, cog: str):
        try:
            await self.bot.unload_extension("commands." + cog)
        except Exception as e:
            return await ctx.send(f"Невозможно выгрузить ког: {traceback.format_exc()}")

        await ctx.send(f"Ког {cog} выгружен")

    @is_owner()
    @hybrid_command(name="reload", description="Перезагружает ког")
    async def reload_reload(self, ctx, cog: str):
        try:
            await self.bot.unload_extension("commands." + cog)
            await self.bot.load_extension("commands." + cog)
        except Exception as e:
            return await ctx.send(f"Невозможно перезагрузить ког {traceback.format_exc()}")

        await ctx.send(f"Ког {cog} перезагружен")


async def setup(bot):
    await bot.add_cog(CogsManagment(bot))
