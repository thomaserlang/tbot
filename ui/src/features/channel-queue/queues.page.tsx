import { Container, Flex, Title } from '@mantine/core'
import { useParams } from 'react-router-dom'
import { useCurrentChannel } from '../channel'
import { QueueView } from './components/queue-view'
import { ChannelQueueId } from './types/queue.types'

export function Component() {
    const channel = useCurrentChannel()
    const { queueId } = useParams<{ queueId?: ChannelQueueId }>()

    return (
        <>
            <title>Queues</title>
            <Container size="sm">
                <Flex
                    h="var(--tbot-content-height)"
                    direction="column"
                    gap="1rem"
                >
                    <Title order={2}>Queues</Title>
                    <QueueView channelId={channel.id} queueId={queueId} />
                </Flex>
            </Container>
        </>
    )
}
