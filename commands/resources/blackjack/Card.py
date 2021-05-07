class Card:
    def __init__(self, pos: int):
        self.value = ['A', '2', '3', '4', '5',
                      '6', '7', '8', '9', '10', 'J', 'Q', 'K'][pos]

    async def getPrice(self) -> int:
        if self.value in ('J', 'Q', 'K'):
            return 10

        if self.value == 'A':
            return 11

        return self.value

    async def show(self) -> str:
        return self.value
