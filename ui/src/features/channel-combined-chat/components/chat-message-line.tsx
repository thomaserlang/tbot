import { ViewerName } from '@/features/channel-viewer/types/viewer.type'
import { Box, MantineFontSize, MantineLineHeight, Text } from '@mantine/core'
import { suggestAAColorVariant } from 'accessible-colors'

import { ChatMessage } from '../types/chat-message.type'
import { AssembleParts } from './assemble-parts'
import { Badges } from './badges'
import classes from './chat-message.module.css'
import { ProviderLogo } from './provider-logo'

interface Props {
    chatMessage: ChatMessage
    hideProviderLogo?: boolean
    hideTime?: boolean
    hideBadges?: boolean
    size?: MantineFontSize & MantineLineHeight
    onViewerClick?: (viewer: ViewerName) => void
}

export function ChatMessageLine({
    chatMessage,
    hideProviderLogo,
    hideTime,
    hideBadges,
    size,
    onViewerClick,
}: Props) {
    return (
        <Box className={classes.message}>
            {!hideTime && (
                <Text
                    component="span"
                    mr="0.25rem"
                    c="dimmed"
                    style={{
                        fontVariantNumeric: 'tabular-nums',
                    }}
                    title={chatMessage.created_at}
                    size={size}
                >
                    {new Date(chatMessage.created_at).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: false,
                    })}
                </Text>
            )}
            {!hideProviderLogo && (
                <ProviderLogo provider={chatMessage.provider} />
            )}
            {!hideBadges && chatMessage.badges.length > 0 && (
                <Badges
                    channelId={chatMessage.channel_id}
                    badges={chatMessage.badges}
                />
            )}
            <Text
                component="span"
                size={size}
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
                    color:
                        suggestAAColorVariant(
                            chatMessage.viewer_color || '',
                            '#1f1f1f'
                        ) || '#8b58FF',
                    cursor: onViewerClick ? 'pointer' : 'default',
                }}
            >
                {chatMessage.viewer_display_name}
            </Text>
            :
            <Text component="span" size={size} className={classes.text}>
                <AssembleParts
                    parts={chatMessage.parts}
                    subType={chatMessage.sub_type}
                />
            </Text>
        </Box>
    )
}
