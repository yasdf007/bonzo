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
                                      {'stop': False, 'win': -1, 'split': False}
                                      ]
        await self.deck.createDeck()

    async def dealToEveryone(self):
        for i in range(0, 2):
            for player in self.players:
                await self.game[player][0].drawCard(await self.deck.draw())
            await self.dealer.drawCard(await self.deck.draw())

    async def checkWithDealer(self):
        dealerScore = self.dealer.sum
        for player in self.players:
            if not self.game[player][1]['split']:
                playerScore = self.game[player][0].sum

                if await self.checkOver21(playerScore):
                    continue
                if ((playerScore > dealerScore) and dealerScore < 21) or (await self.checkOver21(dealerScore) == True and playerScore <= 21):
                    self.game[player][1]['win'] = 1
                    continue
                if ((playerScore == dealerScore) and dealerScore < 21):
                    self.game[player][1]['win'] = 0
                    continue
            else:
                for index, hand in enumerate(self.game[player][0]):
                    playerScore = hand.sum
                    if await self.checkOver21(playerScore):
                        continue
                    if ((playerScore > dealerScore) and dealerScore < 21) or (await self.checkOver21(dealerScore) == True and playerScore <= 21):
                        self.game[player][1]['win'][index] = 1
                        continue
                    if ((playerScore == dealerScore) and dealerScore < 21):
                        self.game[player][1]['win'][index] = 0
                        continue

    async def printGame(self, forceShow=False):
        fields = []
        fields.append({'inline': False, 'name': 'DEALER',
                       'value': f'`{await self.dealer.showHand() if forceShow == False else await self.dealer.getHandAndScore(forceShow)}`'})

        for player in self.players:
            if self.game[player][1]['split']:
                fields.append({'inline': True, 'name': f'{self.ctx.guild.get_member(int(player)).display_name} - 1',
                               'value': f'`{await self.game[player][0][0].getHandAndScore()}`'})

                fields.append({'inline': True, 'name': f'{self.ctx.guild.get_member(int(player)).display_name} - 2',
                               'value': f'`{await self.game[player][0][1].getHandAndScore()}`'})

                continue

            fields.append({'inline': True, 'name': self.ctx.guild.get_member(int(player)).display_name,
                           'value': f'`{await self.game[player][0].getHandAndScore()}`'})

        myDict = {'fields': fields, 'type': 'rich',
                  'title': 'Blackjack'}

        embed = Embed.from_dict(myDict)

        await self.ctx.send(embed=embed)

    async def getResult(self):
        winners = []
        drawList = []
        win = ''
        draw = ''

        for player in self.players:
            if self.game[player][1]['split']:
                for index in range(2):
                    if self.game[player][1]['win'][index] == 1:
                        winners.append(player)
                    if self.game[player][1]['win'][index] == 0:
                        drawList.append(player)
            else:
                if self.game[player][1]['win'] == 1:
                    winners.append(player)
                if self.game[player][1]['win'] == 0:
                    drawList.append(player)
        if len(winners) > 0:
            win = 'Победители: ' + \
                ", ".join([self.ctx.guild.get_member(
                    int(winner)).display_name for winner in winners])
        if len(drawList) > 0:
            draw = 'Ничья: ' + \
                ", ".join([self.ctx.guild.get_member(
                    int(drawP)).display_name for drawP in drawList])

        if winners or drawList:
            return '\n'.join([win, draw])
        return 'Победил DEALER'

    async def splitHand(self, playerId):
        playerHand = self.game[playerId][0]
        hand1 = Hand(dealer=False)
        hand2 = Hand(dealer=False)
        await hand1.drawCard(playerHand.cards[0])
        await hand2.drawCard(playerHand.cards[1])
        await hand1.drawCard(await self.deck.draw())
        await hand2.drawCard(await self.deck.draw())

        self.game[playerId][0] = [
            hand1,
            hand2
        ]

    async def checkFor21(self, score):
        return score == 21

    async def checkOver21(self, score):
        return score > 21

    async def checkForDoubleDown(self, score):
        return 9 <= score <= 11

    async def checkForSplit(self, cards):
        return cards[0].value == cards[1].value

    async def play(self):
        await self.initGame()
        await self.dealToEveryone()

        # self.game[player][0] - инстанс класса Hand
        # self.game[player][1] - словарь из статусов игрока

        for player in self.players:
            doubleDown = False
            split_ = False

            score = await self.game[player][0].getScore()
            if await self.checkFor21(score):
                self.game[player][1]['stop'] = True

            while True:
                if self.game[player][1]['stop'] == True:
                    break

                await self.printGame()
                playerProfile = self.ctx.guild.get_member(int(player))
                msg = f'Ход {playerProfile.mention}\n`h - взять карту, s - не брать (15s)`'

                if not self.game[player][1]['split']:
                    if len(self.game[player][0].cards) == 2:
                        if await self.checkForDoubleDown(score):
                            doubleDown = True
                            msg += '\n`Возможен double down - dd`'

                        if await self.checkForSplit(self.game[player][0].cards):
                            split_ = True
                            msg += '\n`Возможен split - sp`'
                else:
                    msg += f'\n`Рука {handPos+1}`'

                await self.ctx.send(msg)

                try:
                    decicion = await self.ctx.bot.wait_for(
                        'message', check=lambda msg: msg.author.id == int(player) and msg.channel.id == self.ctx.channel.id, timeout=15)

                except asyncio.TimeoutError:
                    self.game[player][1]['stop'] == True
                    await self.ctx.send(f'{playerProfile.display_name} ничего не выбрал')
                    break

                if not self.game[player][1]['split']:
                    if decicion.content.lower() == 'h':
                        await self.game[player][0].drawCard(await self.deck.draw())
                        score = await self.game[player][0].getScore()

                        if await self.checkFor21(score):
                            self.game[player][1]['stop'] = True

                        if await self.checkOver21(score):
                            self.game[player][1]['stop'] = True

                    if decicion.content.lower() == 's':
                        self.game[player][1]['stop'] = True

                    if doubleDown and decicion.content.lower() == 'dd':
                        await self.game[player][0].drawCard(await self.deck.draw())
                        self.game[player][1]['stop'] = True
                        await self.game[player][0].getScore()

                    if split_ and decicion.content.lower() == 'sp':
                        self.game[player][1]['split'] = True
                        self.game[player][1]['win'] = [-1, -1]
                        await self.splitHand(player)
                        handPos = 0

                if self.game[player][1]['split']:
                    if decicion.content.lower() == 'h':
                        await self.game[player][0][handPos].drawCard(await self.deck.draw())
                        score = await self.game[player][0][handPos].getScore()

                        if await self.checkFor21(score):
                            if handPos == 1:
                                self.game[player][1]['stop'] = True
                            handPos = 1

                        if await self.checkOver21(score):
                            if handPos == 1:
                                self.game[player][1]['stop'] = True
                            handPos = 1

                    if decicion.content.lower() == 's':
                        if handPos == 1:
                            self.game[player][1]['stop'] = True
                        handPos = 1

        while await self.dealer.getScore() < 17:
            await self.dealer.drawCard(await self.deck.draw())
        await self.checkWithDealer()
        await self.printGame(forceShow=True)
        result = await self.getResult()
        await self.ctx.send(result)
