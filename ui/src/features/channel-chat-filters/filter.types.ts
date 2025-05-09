import { AccessLevel } from '@/types/access-level.type'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'
import { ChannelId } from '../channel/types/channel.types'
import { ChatFilter } from './filter-registry'

export type ChatFilterId = Branded<string, 'FilterId'>

export interface ChatFilterBase {
    id: ChatFilterId
    type: any // TODO: this should only in in child interfaces
    channel_id: ChannelId
    provider: 'all' | Provider
    name: string
    enabled: boolean
    exclude_access_level: AccessLevel
    warning_enabled: boolean
    warning_message: string
    warning_expire_duration: number
    timeout_message: string
    timeout_duration: number
}

export interface ChatFilterRequestBase {
    type: any // TODO: this should only in in child interfaces
    name?: string
    provider?: 'all' | Provider
    enabled?: boolean
    exclude_access_level?: AccessLevel | string
    warning_enabled?: boolean
    warning_message?: string
    warning_expire_duration?: number
    timeout_message?: string
    timeout_duration?: number
}

export interface ChatFilterMatchResult {
    filter: ChatFilter
    matched: boolean
    sub_id: string
}
