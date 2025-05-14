import { queryClient } from '@/queryclient'
import useWebSocket from 'react-use-websocket'
import { QueueEvent } from '../types/queue-event.types'
import { ChannelQueueId } from '../types/queue.types'
import { getQueueViewersQueryKey } from './queue-viewers.api'

interface GetChatlogsWSProps {
    queueId: ChannelQueueId
}
export function useHandleQueueEvents({ queueId }: GetChatlogsWSProps) {
    useWebSocket(
        `/api/2/channel-queues/${queueId}/events`,
        {
            queryParams: {},
            shouldReconnect: () => true,
            retryOnError: true,
            reconnectInterval: 1000,
            reconnectAttempts: Infinity,
            onOpen: () => {
                queryClient.invalidateQueries({
                    queryKey: getQueueViewersQueryKey({
                        queueId: queueId,
                    }),
                })
            },
            onMessage: (message) => {
                const event = JSON.parse(message.data) as QueueEvent
                if (event.channel_queue_viewer) {
                    queryClient.invalidateQueries({
                        queryKey: getQueueViewersQueryKey({
                            queueId: queueId,
                        }),
                    })
                }
            },
        },
        !!queueId
    )
}
