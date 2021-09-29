"""
basically stole from https://github.com/cloudwithax/pomice
"""


class FilterInvalidArgument(Exception):
    pass


class Filter:

    def __init__(self):
        self.payload = None


class Timescale(Filter):

    def __init__(self, *, speed: float = 1.0, pitch: float = 1.0, rate: float = 1.0):
        super().__init__()

        if speed <= 0:
            raise FilterInvalidArgument(
                "Timescale speed must be more than 0.")
        if pitch <= 0:
            raise FilterInvalidArgument(
                "Timescale pitch must be more than 0.")
        if rate <= 0:
            raise FilterInvalidArgument(
                "Timescale rate must be more than 0.")

        self.speed = speed
        self.pitch = pitch
        self.rate = rate

        self.payload = {"timescale": {"speed": self.speed,
                                      "pitch": self.pitch,
                                      "rate": self.rate}}

    async def set_speed(self, speed):
        self.payload['timescale']['speed'] = speed

    async def set_pitch(self, pitch):
        self.payload['timescale']['pitch'] = pitch

    async def reset_speed(self):
        self.payload['timescale']['speed'] = 1.0

    async def reset_pitch(self):
        self.payload['timescale']['pitch'] = 1.0

    async def reset_filters(self):
        self.payload['timescale']['speed'] = 1.0
        self.payload['timescale']['pitch'] = 1.0

    def __repr__(self):
        return f"<Pomice.TimescaleFilter speed={self.speed} pitch={self.pitch} rate={self.rate}>"
