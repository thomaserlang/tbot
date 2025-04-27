from enum import IntEnum


class TAccessLevel(IntEnum):
    PUBLIC = 0
    SUB = 1
    VIP = 2
    MOD = 7
    ADMIN = 8
    OWNER = 9
    GLOBAL_ADMIN = 1000
