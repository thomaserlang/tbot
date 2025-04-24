export interface TwitchBadge {
    set_id: string
    id: string
    info: string
}

export type TwitchFragmentEmoteFormat = 'animated' | 'static' | string

export interface TwitchFragmentEmote {
    id: string
    emote_set_id: string
    owner_id: string
    format: TwitchFragmentEmoteFormat[]
    externalType?: '7tv'
}

export interface TwitchFragmentCheermote {
    prefix: string
    bits: number
    tier: number
}

export interface TwitchFragmentMention {
    user_id: string
    user_login: string
    user_name: string
}

export type TwitchMessageFragmentType =
    | 'text'
    | 'emote'
    | 'cheermote'
    | 'mention'

export interface TwitchMessageFragment {
    type: TwitchMessageFragmentType
    text: string
    cheermote?: TwitchFragmentCheermote | null
    emote?: TwitchFragmentEmote | null
    mention?: TwitchFragmentMention | null
}

export interface BadgeVersion {
    id: string
    description: string
    title: string
    image_url_1x: string
    image_url_2x: string
    image_url_4x: string
    click_action: string | null
    click_url: string | null
}

export interface Badge {
    set_id: string
    versions: BadgeVersion[]
}

export interface ChannelBadges {
    channel_badges: Badge[]
    global_badges: Badge[]
}

export interface ChatBadge {
    set_id: string
    id: string
    info: string
}
