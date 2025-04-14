import { Provider } from '@/types/provider.type'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { TwitchFragmentEmote } from '../types/twitch.type'

export type EmoteMap = { [key: string]: TwitchFragmentEmote }
export type EmotesResponse = {
    emotes: EmoteMap
    emoteIds: string[]
    regex: RegExp
}

interface GetProps {
    providerId: string
    provider: Provider
}

export async function getEmotes({
    provider,
    providerId,
}: GetProps): Promise<EmotesResponse> {
    const r = await Promise.all([
        get7tvUserEmotes({ provider, providerId }),
        get7tvGlobalEmotes(),
    ])
    const emotes = [...r[0], ...r[1]].reduce((acc, emote) => {
        acc[emote.emote_set_id] = emote
        return acc
    }, {} as EmoteMap)

    return {
        emotes: emotes,
        emoteIds: Object.keys(emotes),
        regex: new RegExp(`(${Object.keys(emotes).join('|')})`),
    } as EmotesResponse
}

async function get7tvUserEmotes({
    provider,
    providerId,
}: GetProps): Promise<TwitchFragmentEmote[]> {
    const r = await axios.get(
        `https://7tv.io/v3/users/${provider}/${providerId}`
    )
    return r.data.emote_set.emotes.map((emote: any) => ({
        id: emote.id,
        emote_set_id: emote.name,
        owner_id: emote.id,
        format: emote.animated ? ['animated'] : ['static'],
        externalType: '7tv',
    })) as TwitchFragmentEmote[]
}

async function get7tvGlobalEmotes(): Promise<TwitchFragmentEmote[]> {
    const r = await axios.get(`https://7tv.io/v3/emote-sets/global`)
    return r.data.emotes.map((emote: any) => ({
        id: emote.id,
        emote_set_id: emote.name,
        owner_id: emote.id,
        format: emote.animated ? ['animated'] : ['static'],
        externalType: '7tv',
    })) as TwitchFragmentEmote[]
}

export function useGetEmotes({ provider, providerId }: GetProps) {
    return useQuery({
        queryKey: ['emotes', provider, providerId],
        queryFn: () => getEmotes({ provider, providerId }),
        staleTime: 1000 * 60 * 5,
        enabled: provider == 'twitch',
    })
}
