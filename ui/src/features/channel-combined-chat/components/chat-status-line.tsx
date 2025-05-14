import { Box, Text } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { AssembleParts } from './assemble-parts'
import classes from './chat-message-line.module.css'
import { ProviderLogo } from './provider-logo'

interface Props {
    chatMessage: ChatMessage
}

export function ChatStatusLine({ chatMessage }: Props) {
    return (
        <Box className={classes.message}>
            <ProviderLogo provider={chatMessage.provider} />
            <Text component="span" c="dimmed">
                <AssembleParts parts={chatMessage.notice_parts} />
            </Text>
        </Box>
    )
}
