import { ChatMessagePart, ChatMessageSubType } from '../types/chat-message.type'

import { ChannelId } from '@/features/channel/types/channel.types'
import { Provider } from '@/types/provider.type'
import { Box, Text } from '@mantine/core'
import classes from './chat-message.module.css'

interface Props {
    parts: ChatMessagePart[]
    subType?: ChatMessageSubType
    channelId?: ChannelId
    provider?: Provider
    providerUserId?: string
}

export function AssembleParts(props: Props) {
    return props.parts.map((part, ix) => (
        <AssemblePart
            key={`${ix}-${part.text}`}
            {...props}
            part={part}
            last={ix === props.parts.length - 1}
        />
    ))
}

interface PartProps extends Omit<Props, 'parts'> {
    part: ChatMessagePart
    last?: boolean
}

function AssemblePart(props: PartProps) {
    switch (props.part.type) {
        case 'emote':
            return <EmotePart {...props} />
        case 'gift':
            return <GiftPart {...props} />
        default:
            return <>{props.part.text}</>
    }
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

export function GiftPart({
    part,
    channelId,
    provider,
    providerUserId,
}: {
    part: ChatMessagePart
    channelId?: ChannelId
    provider?: Provider
    providerUserId?: string
}) {
    if (!channelId || !provider || !providerUserId) return part.text
    const gift = part.gift
    if (!gift) return part.text
    const tiers = [1, 100, 1000, 10000, 100000]
    const tier = tiers
        .filter((t) => gift.count >= t)
        .reduce((max, curr) => Math.max(max, curr), 1)
    return (
        <Box component="span" title={part.text}>
            <img
                src={`/api/2/channels/${channelId}/${provider}/gift-image/${providerUserId}/sm/${gift.id}`}
                alt={part.text}
                className={`${classes.emote} ${classes[`emote-sm`]}`}
            />
            <Text component="span" fw={500} className={classes[`gift-${tier}`]}>
                {gift.count}
            </Text>
        </Box>
    )
}
