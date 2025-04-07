import { toastError } from '@/utils/toast'
import { Button } from '@mantine/core'
import { useGetProviderConnectUrl } from '../provider.api'
import { ChannelProvider } from '../provider.types'

interface Props {
    provider: ChannelProvider
}

export function ProviderView({ provider }: Props) {
    const connectUrl = useGetProviderConnectUrl({
        onSuccess: ({ url }) => {
            window.location.href = url
        },
        onError: (error) => {
            toastError(error)
        },
    })
    return (
        <div>
            {provider.scope_needed && (
                <Button
                    color="green"
                    loading={connectUrl.isPending}
                    onClick={() => {
                        connectUrl.mutate({
                            channelId: provider.channel_id,
                            provider: provider.provider,
                        })
                    }}
                >
                    Reconnect
                </Button>
            )}
        </div>
    )
}
