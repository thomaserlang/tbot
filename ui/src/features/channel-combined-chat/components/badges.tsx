import { ChannelId } from '@/features/channel/types/channel.types'
import { useGetTwitchBadges } from '../api/twitch-badges.api'
import { ChatMessageBadge } from '../types/chat-message.type'
import classes from './chat-message-line.module.css'

interface Props {
    channelId: ChannelId
    badges: ChatMessageBadge[]
}
export function Badges({ channelId, badges }: Props) {
    const channelBadges = useGetTwitchBadges({ channelId })

    if (channelBadges.isLoading) return null

    return (
        <>
            {badges.map((badge) => {
                const badgeVersion =
                    channelBadges.data?.[`${badge.type}/${badge.id}`]
                if (!badgeVersion) return null
                return (
                    <img
                        key={`${badge.type}-${badge.id}`}
                        title={badgeVersion.title}
                        src={badgeVersion.image_url_1x}
                        alt={badgeVersion.id}
                        width={18}
                        height={18}
                        className={classes['chat-badge']}
                    />
                )
            })}
        </>
    )
}
