import { ChannelId } from '@/features/channel/types'
import { toastSuccess } from '@/utils/toast'
import { Button } from '@mantine/core'
import { IconCaretRightFilled } from '@tabler/icons-react'
import { useDeleteQueueViewer } from '../api/queue-viewer.api'
import { useGetQueueViewers } from '../api/queue-viewers.api'
import { ChannelQueueId } from '../types/queue.types'

interface Props {
    channelId: ChannelId
    queueId: ChannelQueueId
}

export function QueueNextViewerButton({ channelId, queueId }: Props) {
    const viewers = useGetQueueViewers({
        channelId,
        queueId,
    })

    const deleteViewer = useDeleteQueueViewer({
        onSuccess: () => {
            if (!viewers.data) return
            if (viewers.data.pages[0].records.length > 1)
                toastSuccess(
                    `Next viewer: ${viewers.data.pages[0].records[1].display_name}`
                )
            else toastSuccess('No more viewers in queue')
        },
        onError: (error) => {
            toastSuccess(error)
        },
    })

    return (
        <Button
            rightSection={<IconCaretRightFilled size={14} />}
            onClick={() => {
                const queueViewerId = viewers.data?.pages[0].records[0].id
                if (!queueViewerId) return
                deleteViewer.mutate({
                    channelId,
                    queueId,
                    queueViewerId,
                })
            }}
            disabled={
                viewers.isLoading || !viewers.data?.pages[0].records.length
            }
            loading={deleteViewer.isPending}
        >
            Next Viewer
        </Button>
    )
}
