import { ViewerName } from '@/features/channel-viewer/types/viewer.type'
import { strDateFormat } from '@/utils/date'
import { Box, Divider } from '@mantine/core'
import { ChatMessage } from '../types/chat-message.type'
import { ChatMessageLine } from './chat-message-line'
import { ChatNoticeLine } from './chat-notice-line'
import { ChatStatusLine } from './chat-status-line'

interface Props {
    messages: ChatMessage[]
    onViewerClick?: (viewer: ViewerName) => void
}

export function ChatMessages({ messages, onViewerClick }: Props) {
    let lastDate = ''
    return (
        <>
            {messages.map((message) => {
                const date = message.created_at.substring(0, 10)
                const showDateLine = date !== lastDate
                if (showDateLine) lastDate = date

                return (
                    <Box p="0.3rem 0" key={message.id}>
                        {showDateLine && (
                            <Divider
                                my="xs"
                                label={strDateFormat(message.created_at)}
                                labelPosition="center"
                            />
                        )}
                        {message.type == 'message' && (
                            <ChatMessageLine
                                chatMessage={message}
                                onViewerClick={onViewerClick}
                            />
                        )}

                        {message.type == 'status' && (
                            <ChatStatusLine chatMessage={message} />
                        )}

                        {message.type == 'notice' && (
                            <ChatNoticeLine chatMessage={message} />
                        )}
                    </Box>
                )
            })}
        </>
    )
}
