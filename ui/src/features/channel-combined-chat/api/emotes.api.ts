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
        getBTTVUserEmotes({ provider, providerId }),
        getBTTVGlobalEmotes(),
    ])
    const emotes = r.flat().reduce((acc, emote) => {
        acc[emote.emote_set_id] = emote
        return acc
    }, {} as EmoteMap)

    return {
        emotes: emotes,
        emoteIds: Object.keys(emotes),
        regex: new RegExp(
            `(?:^|\\s)(${Object.keys(emotes)
                .map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
                .join('|')})(?=$|\\s)`
        ),
    } as EmotesResponse
}

async function get7tvUserEmotes({
    provider,
    providerId,
}: GetProps): Promise<TwitchFragmentEmote[]> {
    try {
        const r = await axios.get(
            `https://7tv.io/v3/users/${provider}/${providerId}`,
            {
                validateStatus: () => true,
            }
        )
        return r.data.emote_set.emotes.map((emote: any) => ({
            id: emote.id,
            emote_set_id: emote.name,
            owner_id: emote.id,
            format: emote.animated ? ['animated'] : ['static'],
            externalType: '7tv',
        })) as TwitchFragmentEmote[]
    } catch (e) {
        return []
    }
}

async function get7tvGlobalEmotes(): Promise<TwitchFragmentEmote[]> {
    try {
        const r = await axios.get(`https://7tv.io/v3/emote-sets/global`)
        return r.data.emotes.map((emote: any) => ({
            id: emote.id,
            emote_set_id: emote.name,
            owner_id: emote.id,
            format: emote.animated ? ['animated'] : ['static'],
            externalType: '7tv',
        })) as TwitchFragmentEmote[]
    } catch (e) {
        return []
    }
}

async function getBTTVGlobalEmotes(): Promise<TwitchFragmentEmote[]> {
    try {
        const r = await axios.get(
            `https://api.betterttv.net/3/cached/emotes/global`
        )
        return r.data.map((emote: any) => ({
            id: emote.id,
            emote_set_id: emote.code,
            owner_id: emote.id,
            format: emote.animated ? ['animated'] : ['static'],
            externalType: 'bttv',
        })) as TwitchFragmentEmote[]
    } catch (e) {
        return []
    }
}

async function getBTTVUserEmotes({
    provider,
    providerId,
}: GetProps): Promise<TwitchFragmentEmote[]> {
    try {
        const r = await axios.get(
            `https://api.betterttv.net/3/cached/users/${provider}/${providerId}`
        )
        const sharedEmotes = r.data.sharedEmotes.map((emote: any) => ({
            id: emote.id,
            emote_set_id: emote.code,
            owner_id: emote.id,
            format: emote.animated ? ['animated'] : ['static'],
            externalType: 'bttv',
        })) as TwitchFragmentEmote[]
        const channelEmotes = r.data.channelEmotes.map((emote: any) => ({
            id: emote.id,
            emote_set_id: emote.code,
            owner_id: emote.id,
            format: emote.animated ? ['animated'] : ['static'],
            externalType: 'bttv',
        })) as TwitchFragmentEmote[]
        return [...sharedEmotes, ...channelEmotes]
    } catch (e) {
        return []
    }
}

export function useGetEmotes({ provider, providerId }: GetProps) {
    return useQuery({
        queryKey: ['emotes', provider, providerId],
        queryFn: () => getEmotes({ provider, providerId }),
        staleTime: 1000 * 60 * 5,
    })
}
