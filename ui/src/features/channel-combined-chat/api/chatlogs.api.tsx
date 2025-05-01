import { ProviderViewerId } from '@/features/channel-viewer/types/viewer.type'
import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { addRecord } from '@/utils/page-records'
import { InfiniteData, useInfiniteQuery } from '@tanstack/react-query'
import useWebSocket from 'react-use-websocket'
import { ChatMessage } from '../types/chat-message.type'

export interface GetChatlogsParams {
    provider?: Provider
    provider_viewer_id?: ProviderViewerId
    type?: string
}

export function getChatlogsQueryKey(
    channelId: ChannelId,
    params?: GetChatlogsParams
) {
    return ['chatlogs', channelId, params]
}

export async function getChatlogs(
    channelId: ChannelId,
    params?: GetChatlogsParams & { cursor?: string }
) {
    const r = await api.get<PageCursor<ChatMessage>>(
        `/api/2/channels/${channelId}/chatlogs`,
        {
            params: {
                per_page: 50,
                ...params,
            },
        }
    )
    return r.data
}

interface GetProps {
    channelId: ChannelId
    params?: GetChatlogsParams
    options?: {
        refetchInterval?: number
    }
}

export function useGetChatlogs({ channelId, params, options }: GetProps) {
    return useInfiniteQuery({
        queryKey: getChatlogsQueryKey(channelId, params),
        queryFn: ({ pageParam }) =>
            getChatlogs(channelId, { ...params, cursor: pageParam }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
        ...options,
    })
}

interface GetChatlogsWSProps {
    channelId: ChannelId
    params?: GetChatlogsParams
    connect?: boolean
}
export function useGetChatlogsWS({
    channelId,
    params,
    connect,
}: GetChatlogsWSProps) {
    useWebSocket(
        `/api/2/channels/${channelId}/chat-ws`,
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
                    queryKey: getChatlogsQueryKey(channelId, params),
                })
            },
            onMessage: (message) => {
                const msg = JSON.parse(message.data) as ChatMessage

                queryClient.setQueryData(
                    getChatlogsQueryKey(channelId, params),
                    (oldData: InfiniteData<PageCursor<ChatMessage>>) => {
                        const exists = oldData.pages[0].records.find(
                            (item) => item.id === msg.id
                        )
                        if (!exists)
                            return addRecord({
                                oldData,
                                data: msg,
                                maxSize: 500,
                            })
                    }
                )
            },
        },
        connect
    )
}
