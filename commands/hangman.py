from discord import Embed, TextChannel
from discord.ext import commands
from random import choice, randint
import asyncio
from commands.resources.hangmanRes import hangmanArr


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hangman = hangmanArr
        self.word = 'пидарас'
        self.dotsInWord = None
        self.gameEmbed = None
        self.letters = None
        self.author = None
        self.lives = None
        self.message = None

    async def makeWord(self):
        # self.word = random...
        # return
        pass

    async def generateHangmanGame(self):
        embed = Embed(title='Виселица', color=randint(0, 0xFFFFFF))
        embed.add_field(
            name='Буквы', value='Тут буквы', inline=True)
        embed.add_field(name='a', value=self.hangman[self.lives], inline=True)
        embed.add_field(name='Угадываемое слово',
                        value=f'{self.dotsInWord} ({len(self.word)} букв)', inline=False)

        return embed

    def check(self, user):
        # id отправителя = id кто поставил эимодзи +
        # id отправителя не равен id бота +
        return user.author.id == self.author.id and user.author.id != self.bot.user.id

    def getLives(self):
        pass

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
            await self.message.edit(embed=Embed(title='Победа'))

    @commands.command(name='hangman', description='Игра виселица')
    async def hangmanLogic(self, ctx):
        self.dotsInWord = '.' * len(self.word)
        self.author = ctx.author
        self.lives = 0
        self.gameEmbed = await self.generateHangmanGame()
        self.message = await ctx.send(embed=self.gameEmbed)

        while True:
            try:
                getLetterFromUser = await self.bot.wait_for('message', timeout=60, check=self.check)
                await TextChannel.purge(ctx.message.channel, limit=1)
                if getLetterFromUser.content == 'стоп':
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
                        if self.lives == 7:
                            await self.message.edit(embed=Embed(title='Проебал'))
                            break
                        # зафигарь ембед новым повешенным
                        # self.lives +=1
                        # chekLives()
                        await ctx.send('lox')
                        await TextChannel.purge(ctx.message.channel, limit=1)
            except asyncio.TimeoutError:
                await ctx.send('время вышло')
                break


def setup(bot):
    bot.add_cog(Hangman(bot))
