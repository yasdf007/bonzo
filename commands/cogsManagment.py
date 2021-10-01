from discord.ext.commands import Cog, command,is_owner
from discord.ext.commands.errors import MissingPermissions



class CogsManagment(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error,MissingPermissions):
            pass
        raise error

    @is_owner()
    @command(name='load', description='Загружает ког')
    async def load_cog(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
        except:
            return await ctx.send('Невозможно загрузить ког')
        
        await ctx.send(f'Ког {cog} загружен')

    @is_owner()
    @command(name='unload', description='Выгружает ког')
    async def unload_cog(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
        except:
            return await ctx.send('Невозможно выгрузить ког')
        
        await ctx.send(f'Ког {cog} выгружен')

    @is_owner()
    @command(name='reload', description='Перезагружает ког')
    async def reload_reload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except:
            return await ctx.send('Невозможно перезагрузить ког')
        
        await ctx.send(f'Ког {cog} перезагружен')


def setup(bot):
    bot.add_cog(CogsManagment(bot))
