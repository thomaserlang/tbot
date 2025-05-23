import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { CurrentUser } from '../current-user.type'

export function getCurrentUserQueryKey() {
    return ['currentUser']
}

export async function getCurrentUser() {
    const response = await api.get<CurrentUser>('/api/2/me')
    return response.data
}

export function useGetCurrentUser() {
    return useQuery({
        queryKey: getCurrentUserQueryKey(),
        queryFn: getCurrentUser,
        refetchOnWindowFocus: false,
    })
}

export async function deleteCurrentUser(username: string) {
    await api.delete(`/api/2/me`, {
        params: {
            username: username,
        },
    })
}

interface DeleteProps {
    username: string
}

export function useDeleteCurrentUser({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: unknown, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: ({ username }: DeleteProps) => deleteCurrentUser(username),
        onSuccess: (data, variables) => {
            onSuccess?.(data, variables)
        },
        onError,
    })
}
