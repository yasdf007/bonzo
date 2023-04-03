from abc import ABC, abstractmethod, abstractproperty

class XpValues(ABC):
    def message_xp(self):
        raise NotImplementedError

    @abstractproperty
    def voice_xp(self):
        raise NotImplementedError

class XpStrategy(ABC):
    @property    
    @abstractmethod
    def xp_values(self):
        raise NotImplementedError
        
    @abstractmethod
    def level_from_xp(xp: int):
        raise NotImplementedError
        
    @abstractmethod
    def xp_from_level(level: int):
        raise NotImplementedError
