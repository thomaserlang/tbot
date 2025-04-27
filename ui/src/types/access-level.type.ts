export enum AccessLevel {
    PUBLIC = 0,
    SUB = 1,
    VIP = 2,
    MOD = 7,
    ADMIN = 8,
    OWNER = 9,
}

export interface AccessLevelInfo {
    value: number
    label: string
}
