import random
from .Card import Card


class Deck:
    deck = []

    async def createDeck(self) -> None:
        for i in range(52):
            self.deck.append(Card(i % 13))
        random.shuffle(self.deck)

    async def draw(self) -> str:
        return self.deck.pop()
