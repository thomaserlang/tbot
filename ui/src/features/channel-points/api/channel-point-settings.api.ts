import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import {
    ChannelPointSettings,
    ChannelPointSettingsUpdate,
} from '../types/channel-point-settings.type'

interface GetProps {
    channelId: string
}

export function getChannelPointSettingsQueryKey({ channelId }: GetProps) {
    return ['channel-point-settings', channelId]
}

export async function getChannelPointSettings({ channelId }: GetProps) {
    const r = await api.get<ChannelPointSettings>(
        `/api/2/channels/${channelId}/point-settings`
    )
    return r.data
}

export function useGetChannelPointSettings({ channelId }: GetProps) {
    return useQuery({
        queryKey: getChannelPointSettingsQueryKey({ channelId }),
        queryFn: () => getChannelPointSettings({ channelId }),
    })
}

interface UpdateProps {
    channelId: string
    data: ChannelPointSettingsUpdate
}

export async function updateChannelPointSettings({
    channelId,
    data,
}: UpdateProps) {
    const r = await api.put<ChannelPointSettings>(
        `/api/2/channels/${channelId}/point-settings`,
        data
    )
    return r.data
}

export function useUpdateChannelPointSettings({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelPointSettings, variables: UpdateProps) => void
    onError?: (error: any, variables: UpdateProps) => void
}) {
    return useMutation({
        mutationFn: updateChannelPointSettings,
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getChannelPointSettingsQueryKey({
                    channelId: variables.channelId,
                }),
                data
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}
