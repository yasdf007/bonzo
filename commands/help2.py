import asyncio
from discord import Embed, File
from discord.ext import commands
from random import randint


class helping2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = ['◀',
                          '▶']
        # Передаем значения из функции в self, чтобы можно было их юзать вне функции
        self.embeds = None
        self.message = None
        self.index = None
        self.author = None

    async def goPrev(self):
        if self.index == 0:
            return
        self.index -= 1
        await self.message.edit(embed=self.embeds[self.index])

    async def goNext(self):
        if self.index != len(self.embeds) - 1:
            self.index += 1
            await self.message.edit(embed=self.embeds[self.index])

    async def addReaction(self):
        for reaction in self.reactions:
            await self.message.add_reaction(reaction)

    def check(self, reaction, user):
        # id отправителя = id кто поставил эимодзи +
        # id отправителя не равен id бота +
        # поставленная реакция есть в пуле реакций
        return user.id == self.author.id and user.id != self.bot.user.id and reaction.emoji in self.reactions

    @commands.command(name='help2', description='Все команды бота')
    async def help2(self, ctx):
        file = File('./static/bonzo.png')

        # Получаем список всех команд из когов
        cogs = [cogg for cogg in self.bot.cogs.keys()]
        # получаем автора сообщения
        self.author = ctx.author
        # получаем ембед
        self.embeds = await self.generateEmbed(cogs)
        # идем с нуля
        self.index = 0
        # отправляем ембед с индексом
        self.message = await ctx.send(embed=self.embeds[self.index])

        #['◀', '▶']
        await self.addReaction()

        while True:
            try:
                add_reaction = await self.bot.wait_for(
                    'reaction_add', timeout=30, check=self.check)

                if add_reaction[0].emoji == '◀':
                    await self.goPrev()
                    await self.message.remove_reaction('◀', self.author)

                elif add_reaction[0].emoji == '▶':
                    await self.goNext()
                    await self.message.remove_reaction('▶', self.author)

            # если timeout (сек) вышел
            except asyncio.TimeoutError:
                await ctx.send('Время вышло')
                break

        # embed.set_footer(text=f"/by bonzo/ for {ctx.message.author}",
        #                  icon_url=ctx.message.author.avatar_url)

        # # Для каждого кога из списка
        # for cog in cogs:
        #     # Ищем команды
        #     cog_command = self.bot.get_cog(cog).get_commands()

        #     # Для каждой команды
        #     for command in cog_command:

        #         # Если есть название и описание команды
        #         if len(command.name) and len(command.description) > 0:

        #             # Если есть другие названия команды
        #             if len(command.aliases) > 0:
        #                 helpAliases = f'{"/".join(command.aliases)}'

        #                 # Отправляем название команд в ембед
        #                 embed.add_field(
        #                     name=f'{command.name}/{helpAliases}', value=f'{command.description}', inline=False)

        #             # Если нет других названий команды
        #             else:
        #                 # Отправляем название команды в ембед
        #                 embed.add_field(
        #                     name=f'{command.name}', value=f'{command.description}', inline=False)

        # embed.add_field(
        #     name='play', value='Проигрывает музыку с YT по запросу (ALPHA)', inline=True)
        # embed.add_field(
        #     name='stop', value='Останавливает воспроизведение', inline=True)

        # message = await ctx.send(embed=embed, file=file)
        # for reaction in reactions:
        #     await message.add_reaction(reaction)

    async def generateEmbed(self, cogsArray):
        embeds = []
        k = 10

        for i in range(0, len(cogsArray), 10):
            embed = Embed(
                title='**Команды бота:**',  # title - головная часть, colour - hex-код цвета полоски
                color=randint(0, 0xFFFFFF))

            embed.set_thumbnail(
                url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")

            currentEmbeds = cogsArray[i:k]
            k += 10

            # Для каждого кога из списка
            for cog in currentEmbeds:
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

            embeds.append(embed)
        return embeds


def setup(bot):
    bot.add_cog(helping2(bot))
