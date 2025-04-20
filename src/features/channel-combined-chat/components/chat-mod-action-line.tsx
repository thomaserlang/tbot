import { Box, Text } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { providerLogo } from './chat-message-line'
import classes from './chat-message-line.module.css'
import { MessageWithFragments } from './message-with-fragments'

interface Props {
    chatMessage: ChatMessage
}

export function ChatModActionLine({ chatMessage }: Props) {
    return (
        <Box className={classes.message}>
            <Text
                component="span"
                mr="0.5rem"
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
                <MessageWithFragments chatMessage={chatMessage} />
            </Text>
        </Box>
    )
}
