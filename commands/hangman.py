from discord import Embed, TextChannel
from discord.ext import commands
from random import choice, randint
import asyncio
from commands.resources.hangmanRes import hangmanArr
from commands.resources.hangmanRes import wordList

name='hangman'
description='Игра виселица [ALPHA]'

class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hangman = hangmanArr
        self.word = wordList
        self.dotsInWord = None
        self.gameEmbed = None
        self.letters = None
        self.author = None
        self.lives = None
        self.message = None

    def makeWord(self):
        self.word = choice(wordList)
        return
        
    def generateHangmanGame(self):
        self.makeWord()
        embed = Embed(title='Виселица', color=randint(0, 0xFFFFFF))
        embed.add_field(
            name='Буквы, которых нет:', value='Недоступно в ALPHA', inline=True)
        embed.add_field(name='Статус:', value=self.hangman[self.lives], inline=True)
        embed.add_field(name='Угадываемое слово',
                        value=f'{self.dotsInWord} (Количество букв: {len(self.word)})', inline=False)

        return embed

    def check(self, user):
        # id отправителя = id кто поставил эимодзи +
        # id отправителя не равен id бота +
        return user.author.id == self.author.id and user.author.id != self.bot.user.id

    def ensureLetterInWord(self, letter):
        if len(letter) > 1:
            return
        if len(letter) < 1:
            return

        counter = 0
        storeCounter = []

        for checkLetter in self.word:
            if checkLetter == letter:
                storeCounter.append(counter)
        # else: - здесь должно быть добавление использованных букв в массив
            counter += 1

        if len(storeCounter) == 0:
            return
        return storeCounter

    async def openLetters(self, positions, letter):
        newWord = list(self.dotsInWord)

        for number in positions:
            newWord[number] = letter

        self.dotsInWord = ''.join(newWord)

        embed = self.message.embeds[0]
        embed.set_field_at(2, name='Угадываемое слово',
                           value=self.dotsInWord, inline=False)
        return embed

    async def checkWord(self):
        if self.word == self.dotsInWord:
            await self.message.edit(embed=Embed(title='Победа :star:', value=f'Ответом было слово: {self.word}'))

    @commands.command(name=name, description=description)
    async def hangmanLogic(self, ctx):
        self.dotsInWord = '.' * len(self.word)
        self.author = ctx.author
        self.lives = 0
        self.gameEmbed = self.generateHangmanGame()
        self.message = await ctx.send(embed=self.gameEmbed)

        while True:
            try:
                getLetterFromUser = await self.bot.wait_for('message', timeout=60, check=self.check)
                await TextChannel.purge(ctx.message.channel, limit=1)
                if getLetterFromUser.content == 'стоп':
                    break
                if getLetterFromUser.content == self.word:
                    await self.message.edit(embed=Embed(title='Победа :star:', value=f'Ответом было слово: {self.word}'))
                    break
                if getLetterFromUser:
                    # на каком(их) местах есть эта буква
                    positions = self.ensureLetterInWord(
                        getLetterFromUser.content)

                    if positions:
                        embed2 = await self.openLetters(positions, getLetterFromUser.content)
                        await self.message.edit(embed=embed2)
                        await self.checkWord()
                    else:
                        self.lives += 1
                        if self.lives == 8:
                            await self.message.edit(embed=Embed(title='Проигрыш :(', value=f'Ответом было слово: {self.word}'))
                            break
                        self.gameEmbed.set_field_at(1, name='Статус:', value=hangmanArr[self.lives], inline=True)
                        self.gameEmbed.set_field_at(2, name='Угадываемое слово',
                            value=f'{self.dotsInWord} (Количество букв: {len(self.word)})', inline=False)
                        await self.message.edit(embed=self.gameEmbed)
                        await ctx.send('Буквы нет')
                        await TextChannel.purge(ctx.message.channel, limit=1)
            except asyncio.TimeoutError:
                await ctx.send('Время вышло')
                break


def setup(bot):
    bot.add_cog(Hangman(bot))
