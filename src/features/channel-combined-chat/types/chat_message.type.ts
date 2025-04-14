import { ChannelId } from '@/features/channel/types'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'
import { TwitchBadge, TwitchMessageFragment } from './twitch.type'

export type ChatMessageId = Branded<string, 'ChatMessageId'>
export type ChatMessageType = 'message' | 'notice' | 'mod_action'
export type ChatterId = Branded<string, 'ChatterId'>

export interface ChatMessage {
    id: ChatMessageId
    type: ChatMessageType
    sub_type: string | null
    provider: Provider
    provider_id: string
    channel_id: ChannelId
    chatter_id: ChatterId
    chatter_name: string
    chatter_display_name: string
    chatter_color: string | null
    message: string
    msg_id: string
    created_at: string
    twitch_badges: TwitchBadge[] | null
    twitch_fragments: TwitchMessageFragment[] | null
}
