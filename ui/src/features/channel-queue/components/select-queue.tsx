import { ChannelId } from '@/features/channel/types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Flex, Select } from '@mantine/core'
import { useGetQueues } from '../api/queues.api'
import { CreateQueueButton } from './create-queue-button'

interface Props {
    channelId: ChannelId
}

export function SelectQueue({ channelId }: Props) {
    const { data } = useGetQueues({
        channelId,
    })

    return (
        <Flex gap="0.5rem">
            <Select
                size="lg"
                placeholder="Select a queue"
                data={pageRecordsFlatten(data).map((item) => ({
                    value: item.id,
                    label: item.name,
                }))}
            />

            <CreateQueueButton channelId={channelId} />
        </Flex>
    )
}
