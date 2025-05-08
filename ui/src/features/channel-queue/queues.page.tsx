import { Container } from '@mantine/core'
import { useParams } from 'react-router-dom'
import { useCurrentChannel } from '../channel'
import { QueueView } from './components/queue-view'
import { ChannelQueueId } from './types/queue.types'

export function Component() {
    const channel = useCurrentChannel()
    const { queueId } = useParams<{ queueId?: ChannelQueueId }>()

    return (
        <Container size="sm">
            <QueueView channelId={channel.id} queueId={queueId} />
        </Container>
    )
}
