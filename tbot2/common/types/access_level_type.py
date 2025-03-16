from enum import Enum


class TAccessLevel(int, Enum):
    PUBLIC = 0
    SUB = 1
    VIP = 2
    MOD = 7
    ADMIN = 8
    OWNER = 9
