from discord import Embed
from discord.ext.commands import Cog, command
from bonzoboot import slash, guilds
from discord_slash import SlashContext, cog_ext
from random import randint
from math import ceil
from commands.resources.paginator import Paginator

name = 'help'
description = 'Все команды бота, инфа о команде help <cmd>'


class helping(Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name=name, description=description, guild_ids=guilds)
    async def help(self, ctx, cmd=None):
        if cmd is None:
            p = Paginator(ctx)
            embeds = await self.generateEmbed(ctx.author)
            for x in embeds:
                p.add_page(x)
            await p.call_controller()

            return

        # проверяем есть ли команда -> получаем инфу о комнде
        cmd = self.bot.get_command(cmd)

        if cmd:
            embed = await self.getCmdEmbed(cmd)

            await ctx.send(embed=embed)

            return

        await ctx.send('Такой команды нет')

    async def getCmdEmbed(self, cmd):
        embed = Embed(title=f'`{cmd}`',
                      description=await self.commandUsage(cmd), color=randint(0, 0xFFFFFF))

        embed.add_field(name='Описание', value=cmd.description, inline=False)

        try:
            subcommands = '\n'.join([str(i) for i in list(cmd.commands)])
            embed.add_field(name='Подкомманды',
                            value=f'`{subcommands}`')
        except:
            pass

        return embed

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

        if len(parameters) > 0:
            parameters = ' '.join(parameters)
            return f'`{commandAndAliases} {parameters}`'

        return f'`{commandAndAliases}`'

    async def generateEmbed(self, author):
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
            embed.set_footer(text=f"/by bonzo/ for {author}  / Page {1 + (i // 10)}/{pages} /",
                             icon_url=author.avatar_url)
            embed.set_thumbnail(
                url="https://i.ibb.co/Xk7qTy4/BOnzo-1.png")

            slicedCommands = allCommands[i:i + 10]

            for command in slicedCommands:
                embed.add_field(
                    name=f'`{ "/".join([command.name, *command.aliases])}`', value=f'{command.description}', inline=False)

            embeds.append(embed)

        return embeds


def setup(bot):
    bot.add_cog(helping(bot))
