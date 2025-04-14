import { Fragment } from 'react/jsx-runtime'
import { EmotesResponse, useGetEmotes } from '../api/emotes.api'
import { ChatMessage } from '../types/chat_message.type'
import {
    TwitchFragmentEmote,
    TwitchMessageFragment,
} from '../types/twitch.type'

import classes from './chat-message-line.module.css'

interface Props {
    chatMessage: ChatMessage
}

export function MessageWithFragments({ chatMessage }: Props) {
    const emotes = useGetEmotes({
        provider: chatMessage.provider,
        providerId: chatMessage.provider_id,
    })
    const fragments = chatMessage.twitch_fragments ?? [
        {
            type: 'text',
            text: chatMessage.message,
        } as TwitchMessageFragment,
    ]
    if (emotes.isError) {
        console.error('Error fetching emotes', emotes.error)
    }

    if (emotes.data)
        return assembleFragments(
            fragments
                .map((fragment) => expandFragments(fragment, emotes.data))
                .flat()
        )
    return <>{chatMessage.message}</>
}

function assembleFragments(fragments: TwitchMessageFragment[]) {
    return fragments.map((fragment, ix) => (
        <Fragment key={`${ix}-${fragment.text}`}>
            {fragment.type !== 'emote' && <>{fragment.text}</>}
            {fragment.type === 'emote' && fragment.emote && (
                <img
                    key={`${ix}-${fragment.emote.id}`}
                    src={getEmoteUrl(fragment.emote, 2)}
                    alt={fragment.text}
                    title={fragment.text}
                    className={classes.emote}
                />
            )}
        </Fragment>
    ))
}

function expandFragments(
    fragment: TwitchMessageFragment,
    emotes: EmotesResponse
): TwitchMessageFragment[] {
    if (fragment.type !== 'text') return [fragment]
    const parts = fragment.text.split(emotes.regex)
    const fragments: TwitchMessageFragment[] = []
    for (const part of parts) {
        if (!part) continue
        if (emotes.emoteIds.includes(part)) {
            fragments.push({
                type: 'emote',
                emote: emotes.emotes[part],
                text: part,
            })
        } else if (part) {
            fragments.push({
                type: 'text',
                text: part,
            })
        }
    }
    return fragments
}

export function getEmoteUrl(emote: TwitchFragmentEmote, size: number): string {
    if (!emote.externalType) {
        return `https://static-cdn.jtvnw.net/emoticons/v2/${emote.id}/default/dark/${size}.0`
    }
    if (emote.externalType === '7tv') {
        return `https://cdn.7tv.app/emote/${emote.id}/${size}x.webp`
    }
    return ''
}
