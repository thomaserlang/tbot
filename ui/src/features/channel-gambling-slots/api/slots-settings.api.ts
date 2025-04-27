import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import {
    SlotsSettings,
    SlotsSettingsUpdate,
} from '../types/slots-settings.type'

interface GetProps {
    channelId: string
}

export function getSlotsSettingsQueryKey({ channelId }: GetProps) {
    return ['slots-settings', channelId]
}

export async function getSlotsSettings({ channelId }: GetProps) {
    const r = await api.get<SlotsSettings>(
        `/api/2/channels/${channelId}/slots-settings`
    )
    return r.data
}

export function useGetSlotsSettings({ channelId }: GetProps) {
    return useQuery({
        queryKey: getSlotsSettingsQueryKey({ channelId }),
        queryFn: () => getSlotsSettings({ channelId }),
    })
}

interface UpdateProps {
    channelId: string
    data: SlotsSettingsUpdate
}

export async function updateSlotsSettings({ channelId, data }: UpdateProps) {
    const r = await api.put<SlotsSettings>(
        `/api/2/channels/${channelId}/slots-settings`,
        data
    )
    return r.data
}

export function useUpdateSlotsSettings({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: SlotsSettings, variables: UpdateProps) => void
    onError?: (error: any, variables: UpdateProps) => void
}) {
    return useMutation({
        mutationFn: updateSlotsSettings,
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getSlotsSettingsQueryKey({
                    channelId: variables.channelId,
                }),
                data
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}
