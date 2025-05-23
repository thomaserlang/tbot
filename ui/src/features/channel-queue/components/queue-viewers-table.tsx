import { RelativeTimeUpdater } from '@/components/relative-time-updater'
import { providerInfo } from '@/constants'
import { ChannelViewerModal } from '@/features/channel-viewer'
import { ChannelId } from '@/features/channel/types/channel.types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { toastError, toastSuccess } from '@/utils/toast'
import { ActionIcon, Anchor, Flex } from '@mantine/core'
import { IconArrowUp, IconX } from '@tabler/icons-react'
import { DataTable } from 'mantine-datatable'
import { useState } from 'react'
import { useHandleQueueEvents } from '../api/queue-events'
import {
    useDeleteQueueViewer,
    useMoveQueueViewerToTop,
} from '../api/queue-viewer.api'
import { useGetQueueViewers } from '../api/queue-viewers.api'
import { QueueViewer } from '../types/queue-viewer.types'
import { ChannelQueueId } from '../types/queue.types'

interface Props {
    channelId: ChannelId
    queueId: ChannelQueueId
}

export function QueueViewersTable({ channelId, queueId: queueId }: Props) {
    const { data } = useGetQueueViewers({
        channelId,
        queueId: queueId,
    })
    useHandleQueueEvents({
        queueId: queueId,
    })
    const deleteViewer = useDeleteQueueViewer({
        onSuccess: () => {
            toastSuccess('Viewer removed from queue')
        },
        onError: (error) => {
            toastError(error)
        },
    })
    const moveToTop = useMoveQueueViewerToTop({
        onSuccess: () => {
            toastSuccess('Viewer moved to top of queue')
        },
        onError: (error) => {
            toastError(error)
        },
    })
    const [viewViewer, setViewViewer] = useState<QueueViewer | null>(null)

    return (
        <>
            {viewViewer && (
                <ChannelViewerModal
                    provider={viewViewer.provider}
                    providerViewerId={viewViewer.provider_viewer_id}
                    opened={!!viewViewer}
                    onClose={() => {
                        setViewViewer(null)
                    }}
                />
            )}

            <DataTable
                records={pageRecordsFlatten(data)}
                highlightOnHover
                withTableBorder
                noHeader
                noRecordsText="No one in queue"
                height="100%"
                fz="md"
                columns={[
                    { accessor: 'position', width: '1%', noWrap: true },
                    {
                        accessor: 'provider',
                        width: '1%',
                        noWrap: true,
                        render: (item) => {
                            if (!item.provider) return null
                            return (
                                <Flex
                                    title={providerInfo[item.provider].name}
                                    c={providerInfo[item.provider].color}
                                >
                                    {providerInfo[item.provider].icon?.({
                                        size: 18,
                                    })}
                                </Flex>
                            )
                        },
                    },
                    {
                        accessor: 'display_name',
                        render: (item) =>
                            item.provider_viewer_id ? (
                                <Anchor
                                    onClick={() => {
                                        setViewViewer(item)
                                    }}
                                >
                                    {item.display_name}
                                </Anchor>
                            ) : (
                                item.display_name
                            ),
                    },
                    {
                        accessor: 'created_at',
                        width: '1%',
                        noWrap: true,
                        render: (item) => (
                            <RelativeTimeUpdater date={item.created_at} />
                        ),
                    },
                    {
                        accessor: '',
                        width: '1%',
                        noWrap: true,
                        render: (item, index) => (
                            <Flex align="center" justify="right">
                                {index !== 0 && (
                                    <ActionIcon
                                        color="var(--text-color)"
                                        size="md"
                                        variant="subtle"
                                        title="Move to top"
                                        loading={moveToTop.isPending}
                                        onClick={() => {
                                            moveToTop.mutate({
                                                channelId,
                                                queueId,
                                                data: {
                                                    channelQueueViewerId:
                                                        item.id,
                                                },
                                            })
                                        }}
                                    >
                                        <IconArrowUp size={16} />
                                    </ActionIcon>
                                )}
                                <ActionIcon
                                    size="md"
                                    color="red"
                                    variant="subtle"
                                    title="Delete from queue"
                                    loading={deleteViewer.isPending}
                                    onClick={() => {
                                        deleteViewer.mutate({
                                            channelId,
                                            queueId,
                                            queueViewerId: item.id,
                                        })
                                    }}
                                >
                                    <IconX size={16} />
                                </ActionIcon>
                            </Flex>
                        ),
                    },
                ]}
            />
        </>
    )
}
