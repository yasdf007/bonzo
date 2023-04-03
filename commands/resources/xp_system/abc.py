from abc import ABC, abstractmethod, abstractproperty

class XpStrategy(ABC):
    @property    
    @abstractmethod
    def message_xp(self):
        raise NotImplementedError
        
    @property    
    @abstractmethod
    def voice_xp(self):
        raise NotImplementedError

    @abstractmethod
    def level_from_xp(xp: int):
        raise NotImplementedError
        
    @abstractmethod
    def xp_from_level(level: int):
        raise NotImplementedError
