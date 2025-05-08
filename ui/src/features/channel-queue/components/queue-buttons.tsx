import { ChannelId } from '@/features/channel/types'
import { Flex } from '@mantine/core'
import { ChannelQueueId } from '../types/queue.types'
import { QueueClearButton } from './queue-clear-button'
import { QueueNextViewerButton } from './queue-next-viewer-button'

interface Props {
    channelId: ChannelId
    queueId: ChannelQueueId
}

export function QueueButtons({ channelId, queueId }: Props) {
    return (
        <Flex gap="1rem">
            <QueueNextViewerButton channelId={channelId} queueId={queueId} />
            <QueueClearButton channelId={channelId} queueId={queueId} />
        </Flex>
    )
}
