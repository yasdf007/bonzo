from pomice import filters

class Bass(filters.Equalizer):
    def __init__(self, *, tag: str, levels: list):
        super().__init__(tag=tag, levels=levels)

    @classmethod
    def bass(cls):
        levels = [(0, 0.2), (1, 0.2), (2, 0.2), (3, 0.2), (4, 0.2),
                  (5, .0), (6, -0.1), (7, -0.25), (8, -0.25), (9, -0.25),
                  (10, -0.25), (11, -0.5), (12, -0.5), (13, -0.5), (14, -0.5)]

        return cls(tag="Bass", levels=levels)


equalizers = {
    'default': filters.Equalizer.flat(),
    'bass': Bass(
            tag="bass",
            levels=[(0, 0.2), (1, 0.2), (2, 0.2), (3, 0.2), (4, 0.2),
                    (5, .0), (6, -0.1), (7, -0.25), (8, -0.25), (9, -0.25),
                    (10, -0.25), (11, -0.5), (12, -0.5), (13, -0.5), (14, -0.5)
            ]
        )
}