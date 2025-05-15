import { Box, Text } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { AssembleParts } from './assemble-parts'
import classes from './chat-message.module.css'
import { ProviderLogo } from './provider-logo'

interface Props {
    chatMessage: ChatMessage
}

export function ChatStatusLine({ chatMessage }: Props) {
    return (
        <Box className={classes.message}>
            <ProviderLogo provider={chatMessage.provider} />
            <Text component="span" c="dimmed">
                <AssembleParts
                    parts={chatMessage.notice_parts}
                    subType={chatMessage.sub_type}
                    channelId={chatMessage.channel_id}
                    provider={chatMessage.provider}
                    providerUserId={chatMessage.provider_id}
                />
            </Text>
        </Box>
    )
}
