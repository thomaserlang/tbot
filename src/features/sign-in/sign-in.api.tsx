import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useMutation } from '@tanstack/react-query'

interface ConnectURL {
    url: string
}

export function useGetSignInUrl({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ConnectURL) => void
    onError?: (error: unknown) => void
} = {}) {
    return useMutation({
        mutationFn: async ({ provider }: { provider: Provider }) => {
            const r = await api.get<ConnectURL>(
                `/api/2/${provider}/sign-in-url`
            )
            return r.data
        },
        onSuccess,
        onError,
    })
}
