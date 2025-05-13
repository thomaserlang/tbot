import { ChannelId } from '@/features/channel/types/channel.types'
import { Skeleton } from '@mantine/core'
import { useGetTwitchBadges } from '../api/twitch-badges.api'
import { ChatMessageBadge } from '../types/chat-message.type'
import classes from './chat-message-line.module.css'

interface Props {
    channelId: ChannelId
    badges: ChatMessageBadge[]
}
export function Badges({ channelId, badges }: Props) {
    const channelBadges = useGetTwitchBadges({ channelId })
    return (
        <>
            {badges.map((badge) => {
                const badgeVersion =
                    channelBadges.data?.[`${badge.type}/${badge.id}`]
                if (!badgeVersion)
                    return (
                        <Skeleton
                            component="span"
                            key={`${badge.type}-${badge.id}`}
                            className={classes['chat-badge']}
                        />
                    )
                return (
                    <img
                        key={`${badge.type}-${badge.id}`}
                        title={badgeVersion?.title || badge.name}
                        src={badgeVersion?.image_url_1x}
                        alt={badge.type}
                        className={classes['chat-badge']}
                    />
                )
            })}
        </>
    )
}
