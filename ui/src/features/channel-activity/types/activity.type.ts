import { ChannelId } from '@/features/channel'
import { ChatMessagePart, MentionPart } from '@/features/channel-chat'
import { DateTimeString } from '@/types/datetime.type'
import { Provider } from '@/types/provider.type'
import { Branded } from '@/utils/brand'

export type ActivityId = Branded<string, 'ActivityId'>

export interface ActivityUpdate {
    read?: boolean
}

export interface Activity {
    id: ActivityId
    channel_id: ChannelId
    provider: Provider
    provider_message_id: string
    provider_user_id: string
    provider_viewer_id: string
    viewer_name: string
    viewer_display_name: string
    type: string
    sub_type: string
    count: number
    count_name: string
    count_decimal_place: number
    count_currency: string | null
    created_at: DateTimeString
    gifted_viewers: MentionPart[] | null
    system_message: string
    message: string | null
    message_parts: ChatMessagePart[] | null
    read: boolean
    color: string
    type_display_name: string
    sub_type_display_name: string
}
