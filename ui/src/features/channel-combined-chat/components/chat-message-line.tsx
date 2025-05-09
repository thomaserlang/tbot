import { providerInfo } from '@/constants'
import { ViewerName } from '@/features/channel-viewer/types/viewer.type'
import { Provider } from '@/types/provider.type'
import { Box, Text } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { Badges } from './badges'
import classes from './chat-message-line.module.css'
import { MessageLine } from './message-line'

interface Props {
    chatMessage: ChatMessage
    onViewerClick?: (viewer: ViewerName) => void
}

export function ChatMessageLine({ chatMessage, onViewerClick }: Props) {
    return (
        <Box className={classes.message}>
            <Text
                component="span"
                mr="0.25rem"
                c="dimmed"
                style={{
                    fontVariantNumeric: 'tabular-nums',
                }}
                title={chatMessage.created_at}
            >
                {new Date(chatMessage.created_at).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false,
                })}
            </Text>
            {providerLogo(chatMessage.provider)}
            {chatMessage.badges && (
                <Badges
                    channelId={chatMessage.channel_id}
                    badges={chatMessage.badges}
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
                <MessageLine chatMessage={chatMessage} />
            </span>
        </Box>
    )
}

export function providerLogo(provider: Provider) {
    return (
        <Box
            component="span"
            className={classes.provider}
            title={providerInfo[provider].name || ''}
            c={providerInfo[provider].color}
        >
            {providerInfo[provider].icon}
        </Box>
    )
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
