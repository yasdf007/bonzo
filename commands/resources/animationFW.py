# Created by vlaner (c) 2020.
# Assisted by yasdf007 (functionalization) and discord.py community (reference onto library)

from asyncio import sleep
from random import randint
from discord import Embed


async def reColoring(x):
    embed = x.embeds[0]
    for _ in range(6):
        newcolor = randint(0, 0xFFFFFF)
        embed.color = newcolor
        await x.edit(embed=embed)
        await sleep(.25)

def randCol():
    return randint(0, 0xFFFFFF)

async def randCol2(x: Embed):
    embed = x.embeds[0]
    embed.color = randint(0, 0xFFFFFF)
    await x.edit(embed=embed)