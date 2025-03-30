import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { ICurrentUser } from './current-user.type'

export function getCurrentUserQueryKey() {
    return ['currentUser']
}

export async function getCurrentUser() {
    const response = await api.get<ICurrentUser>('/api/2/me')
    return response.data
}

export function useGetCurrentUser() {
    return useQuery({
        queryKey: getCurrentUserQueryKey(),
        queryFn: getCurrentUser,
        refetchOnWindowFocus: false,
        retry: false,
    })
}
