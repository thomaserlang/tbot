import { ChannelId } from '@/features/channel/types/channel.types'
import { Provider } from '@/types/provider.type'
import { ChatMessageBadge } from '../types/chat-message.type'
import classes from './chat-message.module.css'

interface Props {
    channelId: ChannelId
    provider: Provider
    providerUserId?: string
    badges: ChatMessageBadge[]
}

export function Badges({ channelId, provider, providerUserId, badges }: Props) {
    return (
        <>
            {badges.map((badge) => {
                return (
                    <img
                        key={`${badge.id}`}
                        title={`${badge.info} ${badge.info}`}
                        src={`/api/2/channels/${channelId}/${provider}/badge-image/${providerUserId}/sm/${badge.id}`}
                        alt={badge.type}
                        className={classes['chat-badge']}
                    />
                )
            })}
        </>
    )
}
