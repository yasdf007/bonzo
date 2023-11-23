from discord.ext.commands import Cog, guild_only
from .resources.blackjack.Blackjack import Blackjack
from discord import app_commands, Interaction, errors
from bot import Bot

import asyncio

class BlackjackCog(Cog):
    group = app_commands.Group(name="blackjack", description="Игра blackjack/21")

    games = {}

    def __init__(self, bot):
        self.bot: Bot = bot

    @group.command(name="start", description="Начать игру blackjack")
    async def start_blackjack(self, inter: Interaction):
        guild_id = str(inter.guild.id)
        if guild_id in self.games:
            await inter.response.send_message('Игра уже идет!', ephemeral=True)
            return
        
        author_id = str(inter.user.id) 
        self.games[guild_id] = [[author_id], {"start": False}]

        while guild_id in self.games:
            try:
                await inter.response.send_message("Ждем игроков 15 секунд, `/blackjack join` для входа в игру")
            except errors.InteractionResponded:
                await inter.followup.send("Ждем игроков 15 секунд, `/blackjack join` для входа в игру")
            await asyncio.sleep(5)

            if not guild_id in self.games:
                break

            if len(self.games[guild_id][0]) == 0:
                self.games.pop(guild_id)
                return

            self.games[guild_id][1] = True
            blackjack = Blackjack(self.bot, inter, players=self.games[guild_id][0])
            await blackjack.play()

            self.games[guild_id][1] = False

    @group.command(name="join", description="Присоединиться к игре blackjack")
    @guild_only()
    async def join(self, inter: Interaction):
        guild_id = str(inter.guild.id)
        if not guild_id in self.games:
            await inter.response.send_message(f"Игра не идет")
            return

        if self.games[guild_id][1] == True:
            await inter.response.send_message(f"Игра идет")
            return

        author_id = str(inter.user.id) 
        if author_id in (self.games[guild_id][0]):
            await inter.response.send_message(f"Уже в игре")
            return

        self.games[guild_id][0].append(author_id)
        await inter.response.send_message(f"Добавил {inter.user}")

    @group.command(name="stop", description="Остановить blackjack")
    @guild_only()
    async def stop(self, inter: Interaction):
        guild_id = str(inter.guild.id)

        if not guild_id in self.games:
            await inter.response.send_message(f"Игра не идет")
            return

        if self.games[guild_id][1] == True:
            await inter.response.send_message(f"Игра идет")
            return

        self.games.pop(guild_id)
        await inter.response.send_message("Игра остановлена")

    @group.command(name="leave", description="Выйти из blackjack")
    async def leave(self, inter: Interaction):
        guild_id = str(inter.guild.id)

        if not guild_id in self.games:
            await inter.response.send_message(f"Игра не идет")
            return

        author_id = str(inter.user.id) 
        if not author_id in self.games[guild_id][0]:
            await inter.response.send_message(f"Ты не в игре")
            return

        if self.games[guild_id][1] == True:
            await inter.response.send_message(f"Игра идет")
            return

        if author_id in (self.games[guild_id][0]):
            self.games[guild_id][0].remove(author_id)
            await inter.response.send_message(f"Удалил {inter.user}")


async def setup(bot):
    await bot.add_cog(BlackjackCog(bot))
