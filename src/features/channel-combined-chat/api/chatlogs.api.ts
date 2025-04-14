import { ChannelId } from '@/features/channel/types'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import useWebSocket from 'react-use-websocket'
import { ChatMessage } from '../types/chat_message.type'

interface Params {
    chatter_id?: string
}

export function getChatlogsQueryKey(channelId: ChannelId, params?: Params) {
    return ['chatlogs', channelId, params]
}

export async function getChatlogs(
    channelId: ChannelId,
    params?: Params & { cursor?: string }
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
    params?: Params
}

export function useGetChatlogs({ channelId, params }: GetProps) {
    return useInfiniteQuery({
        queryKey: getChatlogsQueryKey(channelId, params),
        queryFn: ({ pageParam }) =>
            getChatlogs(channelId, { ...params, cursor: pageParam }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}

interface GetChatlogsWSProps {
    channelId: ChannelId
    onOpen?: () => void
    onClose?: (event: CloseEvent) => void
    onMessage?: (message: ChatMessage) => void
}
export function useGetChatlogsWS({
    channelId,
    onOpen,
    onClose,
    onMessage,
}: GetChatlogsWSProps) {
    useWebSocket(`/api/2/channels/${channelId}/chat-ws`, {
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
    })
}
