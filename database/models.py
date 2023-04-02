from datetime import datetime
from dataclasses import dataclass

@dataclass
class MemberInfo:
    xp: int
    text_xp_at: datetime