import { UserSettings } from '@/features/user/types/user-settings.type'
import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'

export function getUserSettingsQueryKey() {
    return ['user-settings']
}

export async function getUserSettings() {
    const r = await api.get<UserSettings>('/api/2/me/settings')
    return r.data
}

export function useGetUserSettings() {
    return useQuery({
        queryKey: getUserSettingsQueryKey(),
        queryFn: getUserSettings,
    })
}

interface UpdateProps {
    settings: Partial<UserSettings>
}

export async function updateUserSettings({ settings }: UpdateProps) {
    queryClient.setQueryData(
        getUserSettingsQueryKey(),
        (oldData: UserSettings) => ({
            ...oldData,
            ...settings,
        })
    )
    await api.put('/api/2/me/settings', settings)
}

export function useUpdateUserSettings({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: UpdateProps) => void
    onError?: (error: unknown, variables: UpdateProps) => void
} = {}) {
    return useMutation({
        mutationFn: updateUserSettings,
        onSuccess,
        onError,
    })
}
