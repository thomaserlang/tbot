export enum AccessLevel {
    PUBLIC = 0,
    SUB = 1,
    VIP = 2,
    MOD = 7,
    ADMIN = 8,
    OWNER = 9,
}

export const accessLevelLabels: { [level: string]: string } = {
    [AccessLevel.PUBLIC.toString()]: 'Everyone',
    [AccessLevel.SUB.toString()]: 'Subscriber',
    [AccessLevel.VIP.toString()]: 'VIP',
    [AccessLevel.MOD.toString()]: 'Moderator',
    [AccessLevel.ADMIN.toString()]: 'Admin',
    [AccessLevel.OWNER.toString()]: 'Owner',
} as const
