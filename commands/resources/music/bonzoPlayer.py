import pomice
from discord import Message, HTTPException, Embed
from discord.ext.commands import Context
from contextlib import suppress
from datetime import timedelta

class BonzoPlayer(pomice.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.queue = pomice.Queue()
        self.controller: Message = None
        self.context: Context = None

    async def do_next(self) -> None:
        if self.controller:
            with suppress(HTTPException):
                await self.controller.delete()

        try:
            track: pomice.Track = self.queue.get()
        except pomice.QueueEmpty:
            return await self.teardown()
        
        await self.play(track)

        embed = await self.get_controller(track)

        self.controller = await self.context.send(embed=embed)

    async def shuffle(self):
        return self.queue.shuffle()

    async def get_controller(self, track: pomice.Track):
        embed = Embed(title=f"Сейчас играет {track.title}")

        embed.set_thumbnail(url=track.thumbnail)
        embed.add_field(
            name="Продолжительность",
            value=str(timedelta(milliseconds=int(track.length))),
            inline=False
        )
        embed.add_field(name="В очереди", value=str(self.queue.size), inline=False)
        embed.add_field(name="Ссылка на трек", value=f"[Клик]({track.uri})")

        return embed
    
    async def teardown(self):
        with suppress((HTTPException), (KeyError), (pomice.exceptions.NodeRestException)):
            await self.destroy()
            if self.controller:
                await self.controller.delete()

    async def set_context(self, ctx: Context):
        self.context = ctx
