import { AccessLevel } from '@/types/access-level.type'
import { CommandCreate } from './types/command.types'

export const COMMAND_INITIAL_VALUES: CommandCreate = {
    cmds: [],
    patterns: [],
    response: '',
    active_mode: 'always',
    global_cooldown: 5,
    chatter_cooldown: 15,
    mod_cooldown: 0,
    enabled: true,
    public: true,
    access_level: AccessLevel.PUBLIC.toString(),
    provider: 'all',
} as const
