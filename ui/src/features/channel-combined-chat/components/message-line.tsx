import { Fragment } from 'react/jsx-runtime'
import { ChatMessage, ChatMessagePart } from '../types/chat-message.type'

import classes from './chat-message-line.module.css'

interface Props {
    chatMessage: ChatMessage
}

export function MessageLine({ chatMessage }: Props) {
    return assembleParts(chatMessage.parts)
}

function assembleParts(parts: ChatMessagePart[]) {
    return parts.map((part, ix) => (
        <Fragment key={`${ix}-${part.text}`}>
            {part.type !== 'emote' && <>{part.text}</>}
            {part.type === 'emote' && part.emote && (
                <img
                    key={`${ix}-${part.emote.id}`}
                    src={part.emote.urls?.sm}
                    alt={part.text}
                    title={part.text}
                    className={classes.emote}
                />
            )}
        </Fragment>
    ))
}
