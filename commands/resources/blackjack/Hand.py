class Hand:
    def __init__(self, dealer: bool):
        self.cards = []
        self.dealer = dealer
        self.sum = 0

    async def drawCard(self, card) -> None:
        self.cards.append(card)

    async def getScore(self) -> int:
        aceCount = 0
        self.sum = 0

        for card in self.cards:
            price = await card.getPrice()
            if price == 11:
                aceCount += 1

            self.sum += int(price)

            while aceCount > 0 and self.sum > 21:
                aceCount -= 1
                self.sum -= 10

        return self.sum

    async def showHand(self, forceShow=False):
        if self.dealer and forceShow == False:
            return ''.join(list(map(lambda x: f'[{x}]', ['HIDDEN', await self.cards[1].show()])))
        else:
            return ''.join(list(map(lambda x: f'[{x}]', [await card.show() for card in self.cards])))

    async def getHandAndScore(self, forceShow=False):
        return f'{await self.showHand(forceShow)} - {await self.getScore()}'
