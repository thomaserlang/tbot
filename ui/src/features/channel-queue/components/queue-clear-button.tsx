import { ChannelId } from '@/features/channel/types/channel.types'
import { toastSuccess } from '@/utils/toast'
import { Button, Text } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import { IconClearAll } from '@tabler/icons-react'
import { useClearQueueViewers } from '../api/queue-viewer.api'
import { useGetQueueViewers } from '../api/queue-viewers.api'
import { ChannelQueueId } from '../types/queue.types'

interface Props {
    channelId: ChannelId
    queueId: ChannelQueueId
}

export function QueueClearButton({ channelId, queueId }: Props) {
    const viewers = useGetQueueViewers({
        channelId,
        queueId,
    })

    const clear = useClearQueueViewers({
        onSuccess: () => {
            toastSuccess('Queue cleared')
        },
        onError: (error) => {
            toastSuccess(error)
        },
    })

    return (
        <Button
            rightSection={<IconClearAll size={14} />}
            variant="default"
            onClick={() => {
                openConfirmModal({
                    title: 'Clear Queue',
                    children: (
                        <Text>Are you sure you want to clear the queue?</Text>
                    ),
                    labels: { confirm: 'Clear Queue', cancel: 'Cancel' },
                    onConfirm: () => {
                        clear.mutate({
                            channelId,
                            queueId,
                        })
                    },
                    confirmProps: {
                        color: 'red',
                    },
                })
            }}
            disabled={
                viewers.isLoading || !viewers.data?.pages[0].records.length
            }
            loading={clear.isPending}
        >
            Clear Queue
        </Button>
    )
}
