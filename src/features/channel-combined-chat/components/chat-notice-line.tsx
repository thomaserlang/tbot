import { Alert, Box, Text } from '@mantine/core'
import { ChatMessage } from '../types/chat_message.type'
import { providerShort } from './chat-message-line'
import classes from './chat-message-line.module.css'
import { MessageWithFragments } from './message-with-fragments'

interface Props {
    chatMessage: ChatMessage
}

export function ChatNoticeLine({ chatMessage }: Props) {
    return (
        <Box className={classes.message}>
            <Alert color="blue" fz="md" mr="1rem">
                <Text>
                    {providerShort(chatMessage.provider)}
                    <MessageWithFragments chatMessage={chatMessage} />
                </Text>
            </Alert>
        </Box>
    )
}
