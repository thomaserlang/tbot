import { ChannelId } from '@/features/channel/types'
import { Flex } from '@mantine/core'
import { useNavigate } from 'react-router-dom'
import { ChannelQueueId } from '../types/queue.types'
import { QueueButtons } from './queue-buttons'
import { QueueCreateButton } from './queue-create-button'
import { QueueCreateCommandButton } from './queue-create-command-button'
import { QueueViewersTable } from './queue-viewers-table'
import { SelectQueue } from './select-queue'

interface Props {
    channelId: ChannelId
    queueId?: ChannelQueueId
}

export function QueueView({ channelId, queueId }: Props) {
    const navigate = useNavigate()

    return (
        <Flex direction="column" gap="1rem" h="var(--tbot-content-height)">
            <Flex gap="1rem">
                <SelectQueue
                    channelId={channelId}
                    autoSelect
                    selectedId={queueId}
                    onSelect={(queue) => {
                        navigate(`/channels/${channelId}/queues/${queue.id}`, {
                            replace: true,
                        })
                    }}
                />

                <QueueCreateButton channelId={channelId} />

                {queueId && (
                    <QueueCreateCommandButton
                        channelId={channelId}
                        queueId={queueId}
                    />
                )}
            </Flex>
            {queueId && (
                <>
                    <QueueButtons channelId={channelId} queueId={queueId} />
                    <QueueViewersTable
                        channelId={channelId}
                        queueId={queueId}
                    />
                </>
            )}
        </Flex>
    )
}
