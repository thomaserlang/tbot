import { ChannelId } from '@/features/channel'
import {
    ChannelProvider,
    ChannelProviderId,
    updateChannelProviderCache,
} from '@/features/channel-provider'
import { api } from '@/utils/api'
import { useMutation } from '@tanstack/react-query'
import { LiveBroadcastInsert } from './youtube.types'

interface CreateParams {
    channelId: ChannelId
    channelProviderId: ChannelProviderId
    data?: LiveBroadcastInsert
}
async function youtubeCreateBroadcast({
    channelId,
    channelProviderId,
    data,
}: CreateParams) {
    const r = await api.post<ChannelProvider>(
        `/api/2/channels/${channelId}/providers/${channelProviderId}/youtube/broadcast`,
        data
    )
    return r.data
}

export function useCreateBroadcast({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelProvider, variables: CreateParams) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: youtubeCreateBroadcast,
        onSuccess: (data, variables) => {
            updateChannelProviderCache(data)
            onSuccess?.(data, variables)
        },
        onError,
    })
}
