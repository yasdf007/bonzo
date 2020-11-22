from discord import Embed
from discord.ext import commands
from random import randint


class helping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help2', description='Все команды бота')
    async def help2(self, ctx):
        embed = Embed(title='Команды', color=randint(0, 0xFFFFFF))

        # Получаем список всех команд из когов
        cogs = [cogg for cogg in self.bot.cogs.keys()]

        embed.set_footer(text=f"/by bonzo/ for {ctx.message.author}",
                         icon_url=ctx.message.author.avatar_url)

        # Для каждого кога из списка
        for cog in cogs:
            # Ищем команды
            cog_command = self.bot.get_cog(cog).get_commands()

            # Для каждой команды
            for command in cog_command:

                # Если есть название и описание команды
                if len(command.name) and len(command.description) > 0:

                    # Если есть другие названия команды
                    if len(command.aliases) > 0:
                        helpAliases = f'{"/".join(command.aliases)}'

                        # Отправляем название команд в ембед
                        embed.add_field(
                            name=f'{command.name}/{helpAliases}', value=f'{command.description}', inline=False)

                    # Если нет других названий команды
                    else:
                        # Отправляем название команды в ембед
                        embed.add_field(
                            name=f'{command.name}', value=f'{command.description}', inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(helping(bot))
