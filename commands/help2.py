import asyncio
from discord import Embed, File
import discord
from discord.ext import commands
from random import randint


class helping2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = ['◀',
                          '▶']
        self.index = 0
        self.embeds = []

    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     if user.id != self.bot.user.id:
    #         print(reaction.emoji, user)
    #         if reaction.emoji == '◀':
    #             await reaction.message.edit(embed=Embed(title='Нажал влево'))
    #         if reaction.emoji == '▶':
    #             await reaction.message.edit(embed=Embed(title='Нажал вправо'))

    async def goPrev(self, message):
        if self.index == 0:
            return
        self.index -= 1
        await message.edit(embed=self.embeds[self.index])

    async def goNext(self, message):
        if self.index != len(self.embeds):
            self.index += 1
            await message.edit(embed=self.embeds[self.index])

    @commands.command(name='help2', description='Все команды бота')
    async def help2(self, ctx):
        file = File('./static/bonzo.png')
        reactions = self.reactions

        # embed = Embed(
        #     title='**Команды бота:**',  # title - головная часть, colour - hex-код цвета полоски
        #     color=randint(0, 0xFFFFFF))
        # embed.set_thumbnail(
        #     url="attachment://bonzo.png")

        # Получаем список всех команд из когов
        cogs = [cogg for cogg in self.bot.cogs.keys()]

        embedList = await self.generateEmbed(cogs)
        index = self.index

        message = await ctx.send(embed=embedList[index])

        def check(reaction, user):
            return user.id == ctx.author.id and user.id != self.bot.user.id and reaction.emoji in reactions

        for reaction in reactions:
            await message.add_reaction(reaction)

        try:
            reactionAdded = await self.bot.wait_for(
                'reaction_add', check=check)
            if reactionAdded[0].emoji == '◀':
                await self.goPrev(message)
                self.index = 0
            elif reactionAdded[0].emoji == '▶':
                await self.goNext(message)
                self.index = 0

        except asyncio.TimeoutError:
            await ctx.send('Время вышло')

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

            self.embeds.append(embed)
        return self.embeds


def setup(bot):
    bot.add_cog(helping2(bot))
