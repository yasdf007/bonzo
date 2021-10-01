from discord import Embed
from .animationFW import randCol

class automata:

    def generateEmbErr(x: str):
        result = Embed(
            title=f'**{x}**',
            color=randCol()
        )
        result.set_footer(text='Error message / by Bonzo /')
        return result

    # def generateEmbInfo(x: str):
    #     result = Embed(
    #         title=f'**{x}**',
    #         color=randCol()
    #     )
    #     result.set_footer(text='')
    #     return result