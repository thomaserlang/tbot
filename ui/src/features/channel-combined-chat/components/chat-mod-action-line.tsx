import { Box, Text } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { providerLogo } from './chat-message-line'
import classes from './chat-message-line.module.css'
import { MessageLine } from './message-line'

interface Props {
    chatMessage: ChatMessage
}

export function ChatModActionLine({ chatMessage }: Props) {
    return (
        <Box className={classes.message}>
            <Text
                component="span"
                mr="0.25rem"
                c="dimmed"
                title={chatMessage.created_at}
            >
                {new Date(chatMessage.created_at).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false,
                })}
            </Text>
            {providerLogo(chatMessage.provider)}
            <Text component="span" c="dimmed">
                <MessageLine chatMessage={chatMessage} />
            </Text>
        </Box>
    )
}
