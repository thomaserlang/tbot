import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex } from '@mantine/core'
import { useDeleteProvider, useGetProviderConnectUrl } from '../provider.api'
import { ChannelProvider } from '../provider.types'

interface Props {
    provider: ChannelProvider
    onDeleted?: () => void
}

export function ButtonAction({ provider, onDeleted }: Props) {
    const connectUrl = useGetProviderConnectUrl({
        onSuccess: ({ url }) => {
            window.location.href = url
        },
        onError: (error) => {
            toastError(error)
        },
    })

    const deleteProvider = useDeleteProvider({
        onSuccess: () => {
            toastSuccess('Provider deleted')
            onDeleted?.()
        },
        onError: (error) => {
            toastError(error)
        },
    })

    return (
        <Flex gap="1rem">
            {provider.scope_needed && (
                <Button
                    color="orange"
                    loading={deleteProvider.isPending}
                    onClick={() => {
                        deleteProvider.mutate({
                            channelId: provider.channel_id,
                            providerId: provider.id,
                        })
                    }}
                >
                    Reconnect needed
                </Button>
            )}

            <Button
                color="red"
                loading={connectUrl.isPending}
                onClick={() => {
                    connectUrl.mutate({
                        channelId: provider.channel_id,
                        provider: provider.provider,
                    })
                }}
            >
                Disconnect
            </Button>
        </Flex>
    )
}
