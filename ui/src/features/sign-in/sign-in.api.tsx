import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useMutation } from '@tanstack/react-query'
import { StringParam, useQueryParam } from 'use-query-params'

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
    const [next] = useQueryParam('next', StringParam)
    return useMutation({
        mutationFn: async ({ provider }: { provider: Provider }) => {
            const r = await api.get<ConnectURL>(
                `/api/2/${provider}/sign-in-url`,
                {
                    params: {
                        redirect_to: `/sign-in/success?next=${encodeURI(
                            next || '/channels'
                        )}`,
                    },
                }
            )
            return r.data
        },
        onSuccess,
        onError,
    })
}
