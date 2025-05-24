import { ProviderViewerId } from '@/features/channel-viewer/types/viewer.type'
import { ChannelId } from '@/features/channel/types/channel.types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { Provider } from '@/types/provider.type'
import { PubSubEvent } from '@/types/pubsub-event.type'
import { api } from '@/utils/api'
import { addRecord, removeRecord, updateRecord } from '@/utils/page-records'
import { InfiniteData, useInfiniteQuery } from '@tanstack/react-query'
import useWebSocket from 'react-use-websocket'
import { ChatMessage } from '../types/chat-message.type'

export interface GetChatMessageParams {
    provider?: Provider
    provider_viewer_id?: ProviderViewerId
    type?: string
}

interface GetProps {
    channelId: ChannelId
    params?: GetChatMessageParams
    options?: {
        refetchInterval?: number
    }
}
export function getChatMessageQueryKey({ channelId }: GetProps) {
    return ['chatlogs', channelId]
}

export async function getChatMessages({
    channelId,
    params,
}: GetProps & {
    params?: GetChatMessageParams & { cursor?: string }
}) {
    const r = await api.get<PageCursor<ChatMessage>>(
        `/api/2/channels/${channelId}/chat-messages`,
        {
            params: {
                per_page: 50,
                ...params,
            },
        }
    )
    return r.data
}

export function useGetChatlogs({ channelId, params, options }: GetProps) {
    return useInfiniteQuery({
        queryKey: getChatMessageQueryKey({ channelId }),
        queryFn: ({ pageParam }) =>
            getChatMessages({
                channelId,
                params: { ...params, cursor: pageParam },
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
        ...options,
    })
}

interface WSChatMessagesProps {
    channelId: ChannelId
    params?: GetChatMessageParams
    connect?: boolean
}

export function useWSChatMessages({
    channelId,
    params,
    connect,
}: WSChatMessagesProps) {
    return useWebSocket(
        `/api/2/channels/${channelId}/chat-messages-ws`,
        {
            queryParams: {
                ...params,
            },
            shouldReconnect: () => true,
            retryOnError: true,
            reconnectInterval: 1000,
            reconnectAttempts: Infinity,
            onOpen: () => {
                queryClient.refetchQueries({
                    queryKey: getChatMessageQueryKey({ channelId, params }),
                })
            },
            onMessage: (message) => {
                const event = JSON.parse(
                    message.data
                ) as PubSubEvent<ChatMessage>

                queryClient.setQueryData(
                    getChatMessageQueryKey({ channelId, params }),
                    (oldData: InfiniteData<PageCursor<ChatMessage>>) => {
                        if (event.action === 'deleted') {
                            return removeRecord({
                                oldData,
                                matchFn: (item) => item.id === event.data.id,
                            })
                        }

                        if (event.action === 'updated') {
                            return updateRecord({
                                oldData,
                                data: event.data,
                                matchFn: (item) => item.id === event.data.id,
                            })
                        }

                        if (event.action === 'new') {
                            const exists = oldData.pages[0].records.find(
                                (item) => item.id === event.data.id
                            )
                            if (!exists)
                                return addRecord({
                                    oldData,
                                    data: event.data,
                                    maxSize: 500,
                                })
                        }
                    }
                )
            },
        },
        connect
    )
}
