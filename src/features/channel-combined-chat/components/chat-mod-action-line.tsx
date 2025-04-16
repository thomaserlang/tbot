import { Box } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { providerShort } from './chat-message-line'
import classes from './chat-message-line.module.css'
import { MessageWithFragments } from './message-with-fragments'

interface Props {
    chatMessage: ChatMessage
}

export function ChatModActionLine({ chatMessage }: Props) {
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
            <span className={classes.dimmed}>
                <MessageWithFragments chatMessage={chatMessage} />
            </span>
        </Box>
    )
}
