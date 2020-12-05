import asyncio
from discord import Embed, File
from discord.utils import get
from discord.ext import commands
from random import randint
from math import ceil

name = 'help'
description = 'Все команды бота [почти рабочий], инфа о команде help <cmd>'


class helping(commands.Cog):
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
        return user.id == self.author.id and user.id != self.bot.user.id and reaction.emoji in self.reactions and reaction.message.id == self.message.id

    @commands.command(name=name, description=description)
    async def help(self, ctx, cmd=None):
        if cmd is None:

            # получаем автора сообщения
            self.author = ctx.author
            # генерируем ембед
            await self.generateEmbed()
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

                    elif add_reaction[0].emoji == '▶':
                        await self.goNext()

                    await self.message.remove_reaction(add_reaction[0], self.author)

                # если timeout (сек) вышел
                except asyncio.TimeoutError:
                    # чистим реакции
                    await self.message.clear_reactions()
                    break
        else:
            # проверяем есть ли команда -> получаем инфу о комнде
            if (cmd := get(self.bot.commands, name=cmd)):

                embed = Embed(title=f'`{cmd}`',
                              description=await self.commandUsage(cmd), color=randint(0, 0xFFFFFF))

                embed.add_field(name='Описание', value=cmd.description)

                await ctx.send(embed=embed)
            # Команды нет
            else:
                await ctx.send('Такой команды нет')

    # Как используется команда
    async def commandUsage(self, cmd):
        # получаем команду и дргуия названия команды в одну переменную
        commandAndAliases = "/".join([str(cmd), *cmd.aliases])
        parameters = []

        # Для пар команда - значение
        for key, value in cmd.params.items():
            # у всех команд первые self, ctx у некоторых
            # self и ctx не нужны
            if key not in ('self', 'ctx'):
                # [] - необязательные, <> - обязательные переменные для функции
                parameters.append(
                    # В функциях указывали None есть переменная необязательна
                    f'[{key}]' if 'None' in str(value) else f'<{key}>')

        parameters = ' '.join(parameters)
        return f'`{commandAndAliases} {parameters}`'

    async def generateEmbed(self):
        embeds = []
        allCommands = sorted(list(self.bot.commands), key=lambda x: x.name)
        # ceil - округляем в большую стороню
        # 17/10 = 1.8 => 2
        # 20/10 = 2 => 2
        # 21/10 = 2.1 => 3
        pages = ceil(len(allCommands) / 10)

        for i in range(0, len(allCommands), 10):
            embed = Embed(
                title='**Команды бота:**',  # title - головная часть, colour - hex-код цвета полоски
                color=randint(0, 0xFFFFFF))

            # i // 10 + 1:
            # 0/10 + 1 = 0 + 1 = 1 page
            # 10/10 +1 = 1 + 1 = 2 page и тд
            embed.set_footer(text=f"/by bonzo/ for {self.author}  / Page {1 + (i // 10)}/{pages} /",
                             icon_url=self.author.avatar_url)
            embed.set_thumbnail(
                url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")

            slicedCommands = allCommands[i:i+10]

            for command in slicedCommands:
                # Если есть название и описание команды
                if command.name and command.description:

                    # Если есть другие названия команды
                    if command.aliases:
                        helpAliases = f'{"/".join(command.aliases)}'

                        # Отправляем название команд в ембед
                        embed.add_field(
                            name=f'`{command.name}/{helpAliases}`', value=f'{command.description}', inline=False)

                    # Если нет других названий команды
                    else:
                        # Отправляем название команды в ембед
                        embed.add_field(
                            name=f'`{command.name}`', value=f'{command.description}', inline=False)

            embeds.append(embed)
        self.embeds = embeds
        return


def setup(bot):
    bot.add_cog(helping(bot))
