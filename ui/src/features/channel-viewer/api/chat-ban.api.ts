import { ChannelProviderId } from '@/features/channel-provider'
import { ChannelId } from '@/features/channel/types'
import { api } from '@/utils/api'
import { useMutation } from '@tanstack/react-query'
import { ProviderViewerId } from '../types/viewer.type'

interface BanProps {
    channelId: ChannelId
    channelProviderId: ChannelProviderId
    providerViewerId: ProviderViewerId
    banDuration?: number | null
}

export async function banUser({
    channelId,
    channelProviderId,
    providerViewerId,
    banDuration,
}: BanProps) {
    await api.post(
        `/api/2/channels/${channelId}/providers/${channelProviderId}/user-ban`,
        {
            provider_viewer_id: providerViewerId,
            ban_duration: banDuration,
        }
    )
}

export function useBanUser({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: BanProps) => void
    onError?: (error: unknown, variables: BanProps) => void
} = {}) {
    return useMutation({
        mutationFn: banUser,
        onSuccess,
        onError,
    })
}

export async function unbanUser({
    channelId,
    channelProviderId,
    providerViewerId,
}: BanProps) {
    await api.delete(
        `/api/2/channels/${channelId}/providers/${channelProviderId}/user-ban`,
        {
            data: {
                provider_viewer_id: providerViewerId,
            },
        }
    )
}

export function useUnbanUser({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: BanProps) => void
    onError?: (error: unknown, variables: BanProps) => void
} = {}) {
    return useMutation({
        mutationFn: unbanUser,
        onSuccess,
        onError,
    })
}
