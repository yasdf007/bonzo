from datetime import time
from .Deck import Deck
from .Hand import Hand
from discord import Embed
import asyncio


class Blackjack:
    def __init__(self, ctx, players):
        self.deck = Deck()
        self.players = players
        self.dealer = None
        self.game = {}
        self.ctx = ctx

    async def initGame(self):
        self.dealer = Hand(dealer=True)
        for player in self.players:
            self.game[str(player)] = [Hand(dealer=False),
                                      {'stop': False, 'win': False}]
        await self.deck.createDeck()

    async def checkFor21(self, score):
        if score == 21:
            return True
        return False

    async def hasLost(self, score):
        if score > 21:
            return True
        return False

    async def dealToEveryone(self):
        for i in range(0, 2):
            for player in self.players:
                await self.game[player][0].drawCard(await self.deck.draw())
            await self.dealer.drawCard(await self.deck.draw())

    async def checkWithDealer(self):
        dealerScore = await self.dealer.getScore()
        for player in self.players:
            playerScore = await self.game[player][0].getScore()
            if (playerScore > dealerScore and await self.hasLost(playerScore) == False) or (await self.hasLost(dealerScore) == True and playerScore <= 21):
                self.game[player][1]['win'] = True

    async def printGame(self, forceShow=False):
        fields = []
        fields.append({'inline': False, 'name': 'DEALER',
                       'value': f'`{await self.dealer.showHand() if forceShow == False else await self.dealer.getHandAndScore(forceShow)}`'})

        for player in self.players:
            fields.append({'inline': True, 'name': self.ctx.guild.get_member(int(player)).display_name,
                           'value': f'`{await self.game[player][0].getHandAndScore()}`'})

        myDict = {'fields': fields, 'type': 'rich',
                  'title': 'Blackjack'}

        embed = Embed.from_dict(myDict)

        await self.ctx.send(embed=embed)

    async def getWinners(self):
        winners = []
        for player in self.players:
            if self.game[player][1]['win'] == True:
                winners.append(player)

        if len(winners) > 0:
            return ", ".join([self.ctx.guild.get_member(int(winner)).display_name for winner in winners])

        return "DEALER"

    async def play(self):
        await self.initGame()
        await self.dealToEveryone()

        # self.game[player][0] - инстанс класса Hand
        # self.game[player][1] - словарь из статусов игрока

        for player in self.players:
            score = await self.game[player][0].getScore()
            if await self.checkFor21(score):
                self.game[player][1]['stop'] = True

            while True:
                if self.game[player][1]['stop'] == True:
                    break

                await self.printGame()
                playerProfile = self.ctx.guild.get_member(int(player))
                await self.ctx.send(f'Ход {playerProfile.mention}\n`h - взять карту, s - не брать (15s)`')

                try:
                    decicion = await self.ctx.bot.wait_for(
                        'message', check=lambda msg: msg.author.id == playerProfile.id and msg.channel.id == self.ctx.channel.id, timeout=15)
                except asyncio.TimeoutError:
                    self.game[player][1]['stop'] == True
                    await self.ctx.send(f'{playerProfile.display_name} ничего не выбрал')
                    break

                if decicion.content.lower() == 'h':
                    await self.game[player][0].drawCard(await self.deck.draw())
                    score = await self.game[player][0].getScore()

                    if await self.checkFor21(score):
                        self.game[player][1]['stop'] = True

                    if await self.hasLost(score):
                        self.game[player][1]['stop'] = True

                if decicion.content.lower() == 's':
                    self.game[player][1]['stop'] = True

        while await self.dealer.getScore() < 17:
            await self.dealer.drawCard(await self.deck.draw())

        await self.checkWithDealer()
        await self.printGame(forceShow=True)
        winners = await self.getWinners()
        await self.ctx.send(f'Победители: {winners}')
