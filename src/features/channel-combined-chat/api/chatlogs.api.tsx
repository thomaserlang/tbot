import { ProviderViewerId } from '@/features/channel-viewer/types/viewer.type'
import { ChannelId } from '@/features/channel/types'
import { PageCursor } from '@/types/page-cursor.type'
import { Provider } from '@/types/provider.type'
import { api } from '@/utils/api'
import { notifications } from '@mantine/notifications'
import { IconCheck } from '@tabler/icons-react'
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
                notifications.update({
                    id: 'chat-reconnect',
                    title: 'Connected to chat',
                    color: 'green',
                    message: '',
                    autoClose: 2000,
                    loading: false,
                    withCloseButton: false,
                })
                onOpen?.()
            },
            onClose: (event) => {
                if (event.code !== 1005)
                    notifications.show({
                        id: 'chat-reconnect',
                        color: 'blue',
                        loading: true,
                        title: 'Disconnected from chat',
                        message: 'Trying to reconnect',
                        autoClose: false,
                        withCloseButton: true,
                        position: 'bottom-right',
                        icon: <IconCheck size={18} />,
                    })
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
