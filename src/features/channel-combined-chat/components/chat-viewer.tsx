import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ViewerName } from '@/features/channel-viewer/types/viewer.type'
import { ChannelId } from '@/features/channel/types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Flex, Text } from '@mantine/core'
import { notifications } from '@mantine/notifications'
import { IconCheck, IconMessage } from '@tabler/icons-react'
import { useEffect, useRef, useState } from 'react'
import { VList, VListHandle } from 'virtua'
import {
    GetChatlogsParams,
    useGetChatlogs,
    useGetChatlogsWS,
} from '../api/chatlogs.api'
import { ChatMessage } from '../types/chat-message.type'
import { ChatMessages } from './chat-messages'
import { LoadMoreButton } from './load-more-button'
import { ResumeChatButton } from './resume-chat-button'

interface Props {
    channelId: ChannelId
    liveUpdates?: boolean
    params?: GetChatlogsParams
    onViewerClick?: (viewer: ViewerName) => void
}

export function ChatViewer({
    channelId,
    liveUpdates,
    params,
    onViewerClick,
}: Props) {
    const viewport = useRef<VListHandle>(null)
    const data = useGetChatlogs({
        channelId,
        params,
    })
    useEffect(() => {
        if (data.data) {
            setMessages(pageRecordsFlatten(data.data).reverse())
        }
    }, [data.data])

    useGetChatlogsWS({
        channelId,
        connect: liveUpdates,
        params,
        onOpen: () => {
            notificationReconnected()
        },
        onClose: (event) => {
            if (event.code === 1005) return
            notificationShowReconnect()
        },
        onMessage: (message) => {
            setMessages((prev) => [...(prev || []), message].slice(-1000))
        },
    })

    const [autoScroll, setAutoScroll] = useState(true)
    const [messages, setMessages] = useState<ChatMessage[] | undefined>(
        undefined
    )
    const scrollToBottom = () => {
        if (messages !== undefined) {
            viewport.current?.scrollToIndex(messages.length - 1, {
                align: 'end',
            })
        }
    }
    useEffect(() => {
        if (autoScroll) scrollToBottom()
    }, [messages])

    if (data.isLoading || messages === undefined) return <PageLoader />
    if (data.error) return <ErrorBox errorObj={data.error} />

    if (messages.length === 0)
        return (
            <Flex justify="center" align="center" direction="column" gap="1rem">
                <IconMessage size={80} />
                <Text size="xl" fw={500}>
                    No chat messages
                </Text>
            </Flex>
        )

    return (
        <>
            <VList
                ref={viewport}
                style={{ height: '100%' }}
                shift={!autoScroll}
                onScroll={() => {
                    if (viewport.current) {
                        const distanceFromBottom =
                            viewport.current.scrollSize -
                            (viewport.current.scrollOffset +
                                viewport.current.viewportSize)
                        setAutoScroll(distanceFromBottom < 100)
                    }
                }}
            >
                {data.hasNextPage && (
                    <LoadMoreButton onClick={() => data.fetchNextPage()} />
                )}
                {data.isFetchingNextPage && <PageLoader />}
                <ChatMessages
                    messages={messages}
                    onViewerClick={onViewerClick}
                />
            </VList>

            {!autoScroll && (
                <ResumeChatButton
                    onClick={() => {
                        setAutoScroll(true)
                        scrollToBottom()
                    }}
                />
            )}
        </>
    )
}

function notificationShowReconnect() {
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
}

function notificationReconnected() {
    notifications.update({
        id: 'chat-reconnect',
        title: 'Connected to chat',
        color: 'green',
        message: '',
        autoClose: 2000,
        loading: false,
        withCloseButton: false,
    })
}
