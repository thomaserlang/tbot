import { Fragment } from 'react/jsx-runtime'
import { ChatMessagePart, ChatMessageSubType } from '../types/chat-message.type'

import { Box } from '@mantine/core'
import classes from './chat-message.module.css'

interface Props {
    parts: ChatMessagePart[]
    subType?: ChatMessageSubType
}

export function AssembleParts({ parts, subType }: Props) {
    return parts.map((part, ix) => (
        <Fragment key={`${ix}-${part.text}`}>
            {part.type !== 'emote' && <>{part.text}</>}
            {part.type === 'emote' && (
                <EmotePart
                    part={part}
                    subType={subType}
                    last={ix === parts.length - 1}
                />
            )}
        </Fragment>
    ))
}

export function EmotePart({
    part,
    subType,
    last,
}: {
    part: ChatMessagePart
    subType?: ChatMessageSubType
    last?: boolean
}) {
    if (!part.emote) return null

    const size = last && subType == 'power_ups_gigantified_emote' ? 'lg' : 'sm'

    if (size === 'lg') {
        return (
            <Box>
                <img
                    src={part.emote.urls?.[size]}
                    alt={part.text}
                    title={part.text}
                    className={`${classes.emote} ${classes[`emote-${size}`]}`}
                />
            </Box>
        )
    }

    return (
        <img
            src={part.emote.urls?.[size]}
            alt={part.text}
            title={part.text}
            className={`${classes.emote} ${classes[`emote-${size}`]}`}
        />
    )
}
