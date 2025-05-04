import { ChannelId } from '@/features/channel/types'
import { api } from '@/utils/api'
import { useMutation } from '@tanstack/react-query'
import { ChannelProvider, ChannelProviderId } from '../channel-provider.types'

interface RunProps {
    length: number
}

export async function runCommercial(
    channelId: ChannelId,
    channelProviderId: ChannelProviderId,
    data: RunProps
) {
    const r = await api.post<ChannelProvider>(
        `/api/2/channels/${channelId}/providers/${channelProviderId}/run-commercial`,
        data
    )
    return r.data
}

interface UpdateProps {
    channelId: ChannelId
    channelProviderId: ChannelProviderId
    data: RunProps
}

export function useRunCommercial({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelProvider, variables: UpdateProps) => void
    onError?: (error: unknown, variables: UpdateProps) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, channelProviderId, data }: UpdateProps) =>
            runCommercial(channelId, channelProviderId, data),
        onSuccess,
        onError,
    })
}
