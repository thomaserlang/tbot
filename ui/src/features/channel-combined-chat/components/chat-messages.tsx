import { ViewerName } from '@/features/channel-viewer/types/viewer.type'
import { strDateFormat } from '@/utils/date'
import { Box, Divider, Flex } from '@mantine/core'
import { Fragment } from 'react/jsx-runtime'
import { ChatMessage } from '../types/chat-message.type'
import { ChatMessageLine } from './chat-message-line'
import classes from './chat-message.module.css'
import { ChatNoticeLine } from './chat-notice-line'
import { ChatStatusLine } from './chat-status-line'

interface Props {
    messages: ChatMessage[]
    onViewerClick?: (viewer: ViewerName) => void
}

export function ChatMessages({ messages, onViewerClick }: Props) {
    let lastDate = ''
    return (
        <Flex gap="0.6rem" direction="column" mb="1rem">
            {messages.map((message) => {
                const date = message.created_at.substring(0, 10)
                const showDateLine = date !== lastDate
                if (showDateLine) lastDate = date

                return (
                    <Fragment key={message.id}>
                        {showDateLine && (
                            <Divider
                                my="xs"
                                label={strDateFormat(message.created_at)}
                                labelPosition="center"
                                key={message.created_at}
                            />
                        )}

                        <DecorateMessage message={message}>
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
                        </DecorateMessage>
                    </Fragment>
                )
            })}
        </Flex>
    )
}

function DecorateMessage({
    message,
    children,
}: {
    children: React.ReactNode
    message: ChatMessage
}) {
    if (message.sub_type == 'power_ups_message_effect')
        return (
            <Box p="1rem">
                <Box className={classes['message-animated-shadow']}>
                    {children}
                </Box>
            </Box>
        )
    if (message.sub_type == 'channel_points_highlighted')
        return (
            <Box m="0 1rem 0 1rem" className={classes.highlight}>
                {children}
            </Box>
        )
    if (message.type !== 'notice')
        return <Box m="0 1rem 0 1rem">{children}</Box>
    return <Box>{children}</Box>
}
