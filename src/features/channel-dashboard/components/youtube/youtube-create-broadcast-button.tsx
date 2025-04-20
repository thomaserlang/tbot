import { ChannelProvider } from '@/features/channel-providers'
import { toastError, toastSuccess } from '@/utils/toast'
import { Button } from '@mantine/core'
import { useCreateBroadcast } from './youtube.api'

interface Props {
    channelProvider: ChannelProvider
}

export function YoutubeCreateBroadcastButton({ channelProvider }: Props) {
    const create = useCreateBroadcast({
        onSuccess: () => {
            toastSuccess('Broadcast created')
        },
        onError: (error) => {
            toastError(error)
        },
    })

    if (channelProvider.stream_id) return

    return (
        <Button
            loading={create.isPending}
            onClick={() => {
                create.mutate({
                    channelId: channelProvider.channel_id,
                    channelProviderId: channelProvider.id,
                })
            }}
        >
            Create Broadcast
        </Button>
    )
}
