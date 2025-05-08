import { ChannelId } from '@/features/channel/types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Select } from '@mantine/core'
import { useEffect } from 'react'
import { useGetQueues } from '../api/queues.api'
import { ChannelQueueId, Queue } from '../types/queue.types'

interface Props {
    channelId: ChannelId
    selectedId?: ChannelQueueId
    autoSelect?: boolean
    onSelect?: (channelQueue: Queue) => void
}

export function SelectQueue({
    channelId,
    autoSelect,
    selectedId,
    onSelect,
}: Props) {
    const { data } = useGetQueues({
        channelId,
    })
    const records = pageRecordsFlatten(data)
    useEffect(() => {
        if (autoSelect && !selectedId) {
            if (records.length > 0) {
                onSelect?.(records[0])
            }
        }
    }, [data])

    return (
        <Select
            placeholder="Select a queue"
            data={records.map((item) => ({
                value: item.id,
                label: item.name,
            }))}
            value={selectedId}
            onChange={(val) => {
                onSelect?.(records.find((item) => item.id === val) as Queue)
            }}
        />
    )
}
