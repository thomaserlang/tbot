import { ViewerName } from '@/features/channel-viewer/types/viewer.type'
import { Provider } from '@/types/provider.type'
import { Box } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { Badges } from './badges'
import classes from './chat-message-line.module.css'
import { MessageWithFragments } from './message-with-fragments'

interface Props {
    chatMessage: ChatMessage
    onViewerClick?: (viewer: ViewerName) => void
}

export function ChatMessageLine({ chatMessage, onViewerClick }: Props) {
    return (
        <Box className={classes.message}>
            <span className={classes.dimmed} title={chatMessage.created_at}>
                {new Date(chatMessage.created_at).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false,
                })}
            </span>
            {providerShort(chatMessage.provider)}
            {chatMessage.twitch_badges && (
                <Badges
                    channelId={chatMessage.channel_id}
                    badges={chatMessage.twitch_badges}
                />
            )}
            <span
                className={classes.username}
                onClick={() => {
                    onViewerClick?.({
                        provider: chatMessage.provider,
                        provider_viewer_id: chatMessage.provider_viewer_id,
                        name: chatMessage.viewer_name,
                        display_name: chatMessage.viewer_display_name,
                    } as ViewerName)
                }}
                style={{
                    color: fixColor(chatMessage.viewer_color) || '',
                    cursor: onViewerClick ? 'pointer' : 'default',
                }}
            >
                {chatMessage.viewer_display_name}
            </span>
            :
            <span className={classes.text}>
                <MessageWithFragments chatMessage={chatMessage} />
            </span>
        </Box>
    )
}

export function providerShort(provider: Provider) {
    switch (provider) {
        case 'twitch':
            return (
                <span
                    className={`${classes.provider} ${classes.twitch}`}
                    title="Twitch"
                >
                    T
                </span>
            )
        case 'youtube':
            return (
                <span
                    className={`${classes.provider} ${classes.youtube}`}
                    title="YouTube"
                >
                    Y
                </span>
            )
    }
}

function fixColor(color: string | null) {
    switch ((color || '').toUpperCase()) {
        case '#0000FF':
            return '#8b58FF'
        case '#8A2BE2':
            return '#8B58FF'
        case '#000000':
            return '#7A7A7A'
        case '#3A2B2B':
            return '#877587'
        case '#893939':
            return '#B7625F'
        case '#4D4C4D':
            return '#7D7E7F'
        case '#191D59':
            return '#837AC3'
        case '#0E3820':
            return '#5B8969'
        case '#161917':
            return '#7A7A7A'
        case '#5900FF':
            return '#9F4EFF'
        case '#2626D3':
            return '#8061FF'
        case '#1926B3':
            return '#866FFF'
        case '#000061':
            return '#8C68D9'
        default:
            return color
    }
}
