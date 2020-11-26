from discord import Embed, TextChannel
from discord.ext import commands
from random import choice, randint
import asyncio
from commands.resources.hangmanRes import hangmanArr
from commands.resources.hangmanRes import wordList

name = 'hangman'
description = 'Игра виселица [ALPHA]'


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hangman = hangmanArr
        self.word = None
        self.dotsInWord = None
        self.gameEmbed = None
        self.letters = None
        self.author = None
        self.lives = None
        self.botMessage = None
        self.embedWin = None

    def generateHangmanGame(self):
        embed = Embed(title='Виселица', color=randint(0, 0xFFFFFF))
        embed.add_field(
            name='Буквы, которых нет:', value='Недоступно в ALPHA', inline=True)
        embed.add_field(
            name='Статус:', value=self.hangman[self.lives], inline=True)
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

    def openLetters(self, positions, letter):
        newWord = list(self.dotsInWord)

        for number in positions:
            newWord[number] = letter

        self.dotsInWord = ''.join(newWord)

        self.gameEmbed.set_field_at(2, name='Угадываемое слово',
                                    value=f'{self.dotsInWord} (Количество букв: {len(self.word)})', inline=False)
        return

    async def checkWord(self):
        if self.word == self.dotsInWord:
            return True
        else:
            return False

    def setHangMan(self):
        self.gameEmbed.set_field_at(
            1, name='Статус:', value=hangmanArr[self.lives], inline=True)

    def assignVars(self):
        self.word = choice(wordList)
        self.dotsInWord = '.'*len(self.word)
        self.lives = 0
        self.gameEmbed = self.generateHangmanGame()

        self.embedWin = Embed(title='Победа :star:')
        self.embedWin.add_field(
            name='КРАСАВА', value=f'Ответом было слово: {self.word}', inline=False)

        self.embedLost = Embed(title='Проигрыш :(')
        self.embedLost.add_field(
            name='НЕ КРАСАВА', value=f'Ответом было слово: {self.word}', inline=False)

    async def hasLost(self):
        if self.lives == 7:
            await self.botMessage.edit(embed=self.embedLost)
            return True
        return False

    async def rules(self):
        pass

    @commands.command(name=name, description=description)
    async def hangmanLogic(self, ctx):
        self.assignVars()
        self.author = ctx.author
        self.botMessage = await ctx.send(embed=self.gameEmbed)

        while True:
            try:
                getLetterFromUser = await self.bot.wait_for('message', timeout=60, check=self.check)
                if len(getLetterFromUser.content) == 1:

                    await getLetterFromUser.delete()

                    if getLetterFromUser:
                        # на каком(их) местах есть эта буква
                        positions = self.ensureLetterInWord(
                            getLetterFromUser.content.lower())

                        if positions:
                            self.openLetters(
                                positions, getLetterFromUser.content)
                            await self.botMessage.edit(embed=self.gameEmbed)

                            if (await self.checkWord()):
                                await self.botMessage.edit(embed=self.embedWin)
                                break
                        else:
                            self.lives += 1
                            self.setHangMan()

                            if await self.hasLost():
                                break

                            await self.botMessage.edit(embed=self.gameEmbed)

                            noLetter = await ctx.send('Буквы нет')
                            await noLetter.delete()

                elif getLetterFromUser.content == 'стоп':
                    await self.botMessage.delete()
                    break
                elif getLetterFromUser.content == self.word:
                    await self.botMessage.edit(embed=self.embedWin)
                    break

            except asyncio.TimeoutError:
                await ctx.send('Время вышло')
                break


def setup(bot):
    bot.add_cog(Hangman(bot))
