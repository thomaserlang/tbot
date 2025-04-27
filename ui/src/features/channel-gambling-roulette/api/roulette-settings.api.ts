import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import {
    RouletteSettings,
    RouletteSettingsUpdate,
} from '../types/roulette-settings.type'

interface GetProps {
    channelId: string
}

export function getRouletteSettingsQueryKey({ channelId }: GetProps) {
    return ['roulette-settings', channelId]
}

export async function getRouletteSettings({ channelId }: GetProps) {
    const r = await api.get<RouletteSettings>(
        `/api/2/channels/${channelId}/roulette-settings`
    )
    return r.data
}

export function useGetRouletteSettings({ channelId }: GetProps) {
    return useQuery({
        queryKey: getRouletteSettingsQueryKey({ channelId }),
        queryFn: () => getRouletteSettings({ channelId }),
    })
}

interface UpdateProps {
    channelId: string
    data: RouletteSettingsUpdate
}

export async function updateRouletteSettings({ channelId, data }: UpdateProps) {
    const r = await api.put<RouletteSettings>(
        `/api/2/channels/${channelId}/roulette-settings`,
        data
    )
    return r.data
}

export function useUpdateRouletteSettings({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: RouletteSettings, variables: UpdateProps) => void
    onError?: (error: any, variables: UpdateProps) => void
}) {
    return useMutation({
        mutationFn: updateRouletteSettings,
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getRouletteSettingsQueryKey({
                    channelId: variables.channelId,
                }),
                data
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}
