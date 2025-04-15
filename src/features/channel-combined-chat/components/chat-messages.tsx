import { strDateFormat } from '@/utils/date'
import { Divider } from '@mantine/core'
import { Fragment } from 'react/jsx-runtime'
import { ChatMessage } from '../types/chat_message.type'
import { ChatMessageLine } from './chat-message-line'
import { ChatModActionLine } from './chat-mod-action-line'
import { ChatNoticeLine } from './chat-notice-line'

interface Props {
    messages: ChatMessage[]
}

export function ChatMessages({ messages }: Props) {
    let lastDate = ''
    return (
        <>
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
                            />
                        )}
                        {message.type == 'message' && (
                            <ChatMessageLine chatMessage={message} />
                        )}

                        {message.type == 'mod_action' && (
                            <ChatModActionLine chatMessage={message} />
                        )}

                        {message.type == 'notice' && (
                            <ChatNoticeLine chatMessage={message} />
                        )}
                    </Fragment>
                )
            })}
        </>
    )
}
