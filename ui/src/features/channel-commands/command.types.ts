import { ChannelId } from '@/features/channel'
import { AccessLevel } from '@/types/access-level.type'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type CommandActiveMode = 'always' | 'online' | 'offline'
export const commandActiveModeLabels: {
    [mode: CommandActiveMode | string]: string
} = {
    always: 'Online & Offline',
    online: 'Online',
    offline: 'Offline',
} as const

export type CommandId = Branded<string, 'CommandId'>

export interface Command {
    id: CommandId
    channel_id: ChannelId
    cmds: string[]
    patterns: string[]
    response: string
    group_name: string
    global_cooldown: number
    chatter_cooldown: number
    mod_cooldown: number
    active_mode: CommandActiveMode
    enabled: boolean
    public: boolean
    access_level: AccessLevel
    provider: 'all' | Provider
    created_at: string // ISO 8601 datetime
    updated_at: string | null // ISO 8601 datetime
}

export interface CommandCreate {
    cmds?: string[]
    patterns?: string[]
    response: string
    group_name?: string | null
    global_cooldown?: number
    chatter_cooldown?: number
    mod_cooldown?: number
    active_mode?: CommandActiveMode
    enabled?: boolean
    public?: boolean
    access_level?: AccessLevel
    provider?: 'all' | Provider
}

export interface CommandUpdate extends Partial<CommandCreate> {}
