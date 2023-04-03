from .abc import XpStrategy

class OriginalXP(XpStrategy):
    message_xp = 1
    voice_xp = 10

    def level_from_xp(self, xp: int):
        return int((xp / 60) ** 0.5)
        
    def xp_from_level(self, lvl: int):
        return int(60 * lvl ** 2)
    