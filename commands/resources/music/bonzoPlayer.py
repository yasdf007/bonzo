from commands.resources.music.filters import Timescale
import wavelink


class BonzoPlayer(wavelink.Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filter = Timescale()

    #### SETS ####
    async def set_speed(self, speed):
        await self.filter.set_speed(speed=speed)

        await self.node._send(op='filters', guildId=str(self.guild_id), **self.filter.payload)

    async def set_pitch(self, pitch):
        await self.filter.set_pitch(pitch=pitch)

        await self.node._send(op='filters', guildId=str(self.guild_id), **self.filter.payload)

    #### RESETS ####
    async def reset_speed(self):
        await self.filter.reset_speed()

        await self.node._send(op='filters', guildId=str(self.guild_id), **self.filter.payload)

    async def reset_pitch(self):
        await self.filter.reset_pitch()

        await self.node._send(op='filters', guildId=str(self.guild_id), **self.filter.payload)

    async def reset_filter(self):
        await self.filter.reset_filters()

        await self.node._send(op='filters', guildId=str(self.guild_id), **self.filter.payload)
