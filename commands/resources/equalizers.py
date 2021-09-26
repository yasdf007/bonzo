from wavelink.eqs import Equalizer


class Eq(Equalizer):
    # 0-14, -0.25 - 1.0
    @classmethod
    def bass(cls):
        levels = [(0, 0.2), (1, 0.2), (2, 0.2), (3, 0.2), (4, 0.2),
                  (5, .0), (6, -0.1), (7, -0.25), (8, -0.25), (9, -0.25),
                  (10, -0.25), (11, -0.5), (12, -0.5), (13, -0.5), (14, -0.5)]

        return cls(levels=levels, name='Bass')


equalizers = {
    'default': Eq.flat(),
    'bass':    Eq.bass()
}
