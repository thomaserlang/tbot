import { ProviderBot } from '@/features/provider-bot/provider-bot.types'
import { getAllPagesCursor } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'

export function getSystemProviderBotsQueryKey() {
    return ['systemProviderBots']
}

export async function getSystemProviderBots() {
    const r = await getAllPagesCursor<ProviderBot>(
        `/api/2/system-bot-providers`
    )
    return r
}

export function useGetSystemProviderBots() {
    return useQuery({
        queryKey: getSystemProviderBotsQueryKey(),
        queryFn: () => getSystemProviderBots(),
    })
}
