import { ProviderViewerId } from '@/features/channel-viewer/types/viewer.type'
import { ChannelId } from '@/features/channel/types'
import { PageCursor } from '@/types/page-cursor.type'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
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
    onOpen?: () => void
    onClose?: (event: CloseEvent) => void
    onMessage?: (message: ChatMessage) => void
}
export function useGetChatlogsWS({
    channelId,
    params,
    connect,
    onOpen,
    onClose,
    onMessage,
}: GetChatlogsWSProps) {
    let timeoutHandler: null | number = null
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
                onOpen?.()
            },
            onClose: (event) => {
                onClose?.(event)
            },
            onMessage: (message) => {
                if (message.type === 'message') {
                    const data = JSON.parse(message.data)
                    onMessage?.(data)
                }
            },
        },
        connect
    )
}
