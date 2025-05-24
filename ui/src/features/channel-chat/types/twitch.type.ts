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
