import { Alert, Box, Text } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { providerLogo } from './chat-message-line'
import classes from './chat-message-line.module.css'
import { MessageLine } from './message-line'

interface Props {
    chatMessage: ChatMessage
}

export function ChatNoticeLine({ chatMessage }: Props) {
    return (
        <Box className={classes.message}>
            <Alert color="blue" fz="md" mr="1rem">
                <Text>
                    {providerLogo(chatMessage.provider)}
                    <MessageLine chatMessage={chatMessage} />
                </Text>
            </Alert>
        </Box>
    )
}
