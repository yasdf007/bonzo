from discord.embeds import Embed
from .res import *
import random
import asyncio


class Hangman:
    def __init__(self, ctx, player):
        self.player = player
        self.ctx = ctx
        self.game = {'state': 0, 'lives': 7}
        self.word = random.choice(words)
        self.hiddenWord = ''.join(['#' for i in range(len(self.word))])
        self.hangmanArray = hangmanStates

    async def printGame(self):
        fields = []
        state = self.game['state']
        fields.append({'inline': True, 'name': 'Слово',
                       'value': self.hiddenWord})
        fields.append({'inline': True, 'name': 'Челик',
                       'value': self.hangmanArray[state]})

        gameDict = {'fields': fields, 'type': 'rich',
                    'title': 'Hangman'}

        embed = Embed.from_dict(gameDict)

        await self.ctx.send(embed=embed)

    async def replaceInHidden(self, index, letter):
        for i in index:
            self.hiddenWord = self.hiddenWord[:i] + \
                letter + self.hiddenWord[i+1:]

    async def findAndReplaceInHiddenWord(self, letter):
        indxs = [i for i, x in enumerate(list(self.word)) if x == letter]

        if len(indxs) > 0:
            await self.replaceInHidden(indxs, letter)

            return True

        return False

    async def play(self):
        while True:
            await self.printGame()

            if self.game['lives'] == 0:
                break

            await self.ctx.send('Введи букву (15с)')

            try:
                decicion = await self.ctx.bot.wait_for(
                    'message', check=lambda msg: msg.author.id == int(self.player) and msg.channel.id == self.ctx.channel.id, timeout=15)
            except asyncio.TimeoutError:
                await self.ctx.send('Время вышло')
                break

            letter = decicion.content.lower()

            if (letter == self.word):
                await self.ctx.send('Победа')
                break

            if not await self.findAndReplaceInHiddenWord(letter):
                self.game['lives'] -= 1
                self.game['state'] += 1

            if (self.hiddenWord == self.word):
                await self.ctx.send('Победа')
                break
        await self.ctx.send(f'Игра кончилась, словом было {self.word}')
