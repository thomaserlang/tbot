import { ChannelId } from '@/features/channel'
import {
    ChannelProvider,
    ChannelProviderId,
    updateChannelProviderCache,
} from '@/features/channel-providers'
import { api } from '@/utils/api'
import { useMutation } from '@tanstack/react-query'

async function youtubeCreateBroadcast(
    channelId: ChannelId,
    channelProviderId: ChannelProviderId
) {
    const r = await api.post<ChannelProvider>(
        `/api/2/channels/${channelId}/providers/${channelProviderId}/youtube/broadcast`
    )
    return r.data
}

interface CreateParams {
    channelId: ChannelId
    channelProviderId: ChannelProviderId
}

export function useCreateBroadcast({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelProvider, variables: CreateParams) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({ channelId, channelProviderId }: CreateParams) => {
            return youtubeCreateBroadcast(channelId, channelProviderId)
        },
        onSuccess: (data, variables) => {
            updateChannelProviderCache(data)
            onSuccess?.(data, variables)
        },
        onError,
    })
}
