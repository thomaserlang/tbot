import { ChannelId } from '@/features/channel/types'
import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { BadgeVersion, ChannelBadges } from '../types/twitch.type'

export function getTwitchBadgesQueryKey(channelId: ChannelId) {
    return ['twitch-badges', channelId]
}

export async function getTwitchBadges(channelId: ChannelId) {
    const r = await api.get<ChannelBadges>(
        `/api/2/channels/${channelId}/twitch-badges`
    )
    return r.data
}

interface GetProps {
    channelId: ChannelId
}
export function useGetTwitchBadges({ channelId }: GetProps) {
    return useQuery({
        queryKey: getTwitchBadgesQueryKey(channelId),
        queryFn: async () => {
            const badges = await getTwitchBadges(channelId)
            const objBadges: { [badgeIdVersion: string]: BadgeVersion } = {}
            badges.global_badges.forEach((badge) => {
                badge.versions.forEach((version) => {
                    objBadges[`${badge.set_id}/${version.id}`] = {
                        ...version,
                    }
                })
            })
            badges.channel_badges.forEach((badge) => {
                badge.versions.forEach((version) => {
                    objBadges[`${badge.set_id}/${version.id}`] = {
                        ...version,
                    }
                })
            })
            return objBadges
        },
        enabled: !!channelId,
        staleTime: 1000 * 60 * 5,
    })
}
