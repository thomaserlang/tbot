import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ViewerName } from '../types/viewer.type'

export function getViewerSearchQueryKey(query: string) {
    return ['viewer-search', query]
}

export async function getViewerSearch(query: string) {
    const r = await api.get<ViewerName[]>(`/api/2/viewer-search`, {
        params: {
            query,
        },
    })
    return r.data
}

interface GetProps {
    query: string
}
export function useGetViewerSearch({ query }: GetProps) {
    return useQuery({
        queryKey: getViewerSearchQueryKey(query),
        queryFn: () => getViewerSearch(query),
        enabled: query.length > 2,
    })
}
