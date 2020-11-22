from discord import Embed
from discord.ext import commands
from random import randint


class helping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help2', description='Все команды бота')
    async def help2(self, ctx, cog='all'):
        embed = Embed(title='Команды', color=randint(0, 0xFFFFFF))

        cogs = [cogg for cogg in self.bot.cogs.keys()]
        embed.set_footer(text=f"/by bonzo/ for {ctx.message.author}",
                         icon_url=ctx.message.author.avatar_url)
        if cog == 'all':
            for cog in cogs:
                cog_command = self.bot.get_cog(cog).get_commands()

                for command in cog_command:
                    if len(command.name) and len(command.description) > 0:
                        if len(command.aliases) > 0:
                            helpAliases = f'{"/".join(command.aliases)}'
                            embed.add_field(
                                name=f'{command.name}/{helpAliases}', value=f'{command.description}', inline=False)
                        else:
                            embed.add_field(
                                name=f'{command.name}', value=f'{command.description}', inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(helping(bot))
