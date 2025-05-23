import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ActivityTypeName } from '../types/activity-type.type'

export function getActivityTypesQueryKey() {
    return ['activity-types']
}

export async function getActivityTypes() {
    const r = await api.get<ActivityTypeName[]>('/api/2/activity-types')
    return r.data
}

export function useGetActivityTypes() {
    return useQuery({
        queryKey: getActivityTypesQueryKey(),
        queryFn: () => getActivityTypes(),
    })
}
