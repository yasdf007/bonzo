from discord import Embed
from discord import Colour

class automata:

    def generateEmbErr(x: str, error=None):
        result = Embed(
            title=f'**{x}**', color=Colour.random()
        )
        if error:
            readableErr = type(error).__name__
            result.set_footer(text=f'Error message / by Bonzo / {readableErr}')
        else:
            result.set_footer(text='Error message / by Bonzo /')
        return result

    # def generateEmbInfo(x: str):
    #     result = Embed(
    #         title=f'**{x}**',
    #         color=randCol()
    #     )
    #     result.set_footer(text='')
    #     return result