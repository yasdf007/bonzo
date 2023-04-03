from .abc import XpStrategy, XpValues

class IntegerXpValues(XpValues):
    message_xp = 1
    voice_xp = 10

class PowerStrategy(XpStrategy):
    xp_values = None

    def __init__(self, xp_values: XpValues):
        self.xp_values = xp_values

    def level_from_xp(self, xp: int):
        return int((xp / 60) ** 0.5)
        
    def xp_from_level(self, lvl: int):
        return int(60 * lvl ** 2)
    
