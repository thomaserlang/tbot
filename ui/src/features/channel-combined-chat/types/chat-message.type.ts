import { ProviderViewerId } from '@/features/channel-viewer/types/viewer.type'
import { ChannelId } from '@/features/channel/types/channel.types'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type ChatMessageId = Branded<string, 'ChatMessageId'>
export type ChatMessageType = 'message' | 'notice' | 'status'
export type ChatMessageSubType =
    | 'custom_reward_redemption'
    | 'sub'
    | 'resub'
    | 'sub_gift'
    | 'community_sub_gift'
    | 'gift_paid_upgrade'
    | 'prime_paid_upgrade'
    | 'pay_it_forward'
    | 'raid'
    | 'unraid'
    | 'announcement'
    | 'bits_badge_tier'
    | 'ban'
    | 'timeout'
    | 'unban'
    | 'untimeout'
    | 'clear'
    | 'emoteonly'
    | 'emoteonlyoff'
    | 'followers'
    | 'followersoff'
    | 'uniquechat'
    | 'uniquechatoff'
    | 'slow'
    | 'slowoff'
    | 'subscribers'
    | 'subscribersoff'
    | 'unraid'
    | 'delete'
    | 'vip'
    | 'unvip'
    | 'raid'
    | 'add_blocked_term'
    | 'add_permitted_term'
    | 'remove_blocked_term'
    | 'remove_permitted_term'
    | 'mod'
    | 'unmod'
    | 'approve_unban_request'
    | 'deny_unban_request'
    | 'warn'
    | null

export interface ChatMessageBadge {
    id: string
    type: string
    name: string
}

export interface EmotePart {
    id: string
    animated: boolean
    emote_provider: string
    urls: {
        sm: string
        md: string
        lg: string
    } | null
}

export interface MentionPart {
    user_id: string
    username: string
    display_name: string
}

export interface GiftPart {
    id: string
    name: string
    type: string
    count: number
}

export interface ChatMessagePart {
    type: 'text' | 'emote' | 'mention' | 'gift'
    text: string
    gift?: GiftPart | null
    emote?: EmotePart | null
    mention?: MentionPart | null
}

export interface ChatMessage {
    id: ChatMessageId
    type: ChatMessageType
    sub_type: ChatMessageSubType
    provider: Provider
    provider_id: string
    channel_id: ChannelId
    provider_viewer_id: ProviderViewerId
    viewer_name: string
    viewer_display_name: string
    viewer_color: string | null
    message: string
    msg_id: string
    created_at: string
    parts: ChatMessagePart[]
    badges: ChatMessageBadge[]
    notice_message: string
    notice_parts: ChatMessagePart[]
}
