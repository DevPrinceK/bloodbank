from enum import Enum, auto


class BloodType(Enum):
    A_POSITIVE = auto()
    A_NEGATIVE = auto()
    B_POSITIVE = auto()
    B_NEGATIVE = auto()
    AB_POSITIVE = auto()
    AB_NEGATIVE = auto()
    O_POSITIVE = auto()
    O_NEGATIVE = auto()


class Titles(Enum):
    Mr = auto()
    Mrs = auto()
    Miss = auto()
    Dr = auto()
    Prof = auto()
    Ps = auto()
    Rev = auto()
    Hon = auto()
    Sir = auto()
