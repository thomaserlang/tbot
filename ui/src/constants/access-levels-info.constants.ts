import { AccessLevel, AccessLevelInfo } from '@/types/access-level.type'

export const accessLevelInfo: {
    [level in AccessLevel]: AccessLevelInfo
} = {
    [AccessLevel.PUBLIC]: {
        value: AccessLevel.PUBLIC,
        label: 'Public',
    },
    [AccessLevel.SUB]: {
        value: AccessLevel.SUB,
        label: 'Subscriber',
    },
    [AccessLevel.VIP]: {
        value: AccessLevel.VIP,
        label: 'VIP',
    },
    [AccessLevel.MOD]: {
        value: AccessLevel.MOD,
        label: 'Moderator',
    },
    [AccessLevel.ADMIN]: {
        value: AccessLevel.ADMIN,
        label: 'Admin',
    },
    [AccessLevel.OWNER]: {
        value: AccessLevel.OWNER,
        label: 'Owner',
    },
} as const
