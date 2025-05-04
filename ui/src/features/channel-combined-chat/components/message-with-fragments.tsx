import { Fragment } from 'react/jsx-runtime'
import {
    ChatMessage,
    ChatMessagePart,
    EmotePart,
} from '../types/chat-message.type'

import classes from './chat-message-line.module.css'

interface Props {
    chatMessage: ChatMessage
}

export function MessageWithFragments({ chatMessage }: Props) {
    return assembleParts(chatMessage.parts)
}

function assembleParts(parts: ChatMessagePart[]) {
    return parts.map((part, ix) => (
        <Fragment key={`${ix}-${part.text}`}>
            {part.type !== 'emote' && <>{part.text}</>}
            {part.type === 'emote' && part.emote && (
                <img
                    key={`${ix}-${part.emote.id}`}
                    src={getEmoteUrl(part.emote, 1)}
                    alt={part.text}
                    title={part.text}
                    className={classes.emote}
                />
            )}
        </Fragment>
    ))
}

export function getEmoteUrl(emote: EmotePart, size: number): string {
    switch (emote.emote_provider) {
        case 'twitch':
            return `https://static-cdn.jtvnw.net/emoticons/v2/${emote.id}/default/dark/${size}.0`
        case '7tv':
            return `https://cdn.7tv.app/emote/${emote.id}/${size + 1}x.webp`
        case 'bttv':
            return `https://cdn.betterttv.net/emote/${emote.id}/${
                size + 1
            }x.webp`
        default:
            return ''
    }
}
