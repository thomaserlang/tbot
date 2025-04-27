import { ChannelId } from '@/features/channel/types'
import { api } from '@/utils/api'
import { useMutation } from '@tanstack/react-query'
import { ChannelProvider, ChannelProviderId } from '../channel-provider.types'
import { updateChannelProviderCache } from './channel-provider.api'

interface StreamTitleUpdate {
    stream_title: string
}

export async function updateStreamTitle(
    channelId: ChannelId,
    channelProviderId: ChannelProviderId,
    data: StreamTitleUpdate
) {
    const r = await api.put<ChannelProvider>(
        `/api/2/channels/${channelId}/providers/${channelProviderId}/stream-title`,
        data
    )
    return r.data
}

interface UpdateProps {
    channelId: ChannelId
    channelProviderId: ChannelProviderId
    data: StreamTitleUpdate
}

export function useUpdateStreamTitle({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelProvider, variables: UpdateProps) => void
    onError?: (error: unknown, variables: UpdateProps) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, channelProviderId, data }: UpdateProps) =>
            updateStreamTitle(channelId, channelProviderId, data),
        onSuccess: (data, variables) => {
            updateChannelProviderCache(data)
            onSuccess?.(data, variables)
        },
        onError,
    })
}
