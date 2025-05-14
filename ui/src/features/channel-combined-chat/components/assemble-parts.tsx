import { Fragment } from 'react/jsx-runtime'
import { ChatMessagePart } from '../types/chat-message.type'

import classes from './chat-message-line.module.css'

interface Props {
    parts: ChatMessagePart[]
}

export function AssembleParts({ parts }: Props) {
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
