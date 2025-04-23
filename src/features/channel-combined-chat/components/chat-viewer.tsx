import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ViewerName } from '@/features/channel-viewer/types/viewer.type'
import { ChannelId } from '@/features/channel/types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Flex, Text } from '@mantine/core'
import { IconMessage } from '@tabler/icons-react'
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

    useGetChatlogsWS({
        channelId,
        connect: liveUpdates,
        params,
        onOpen: () => {
            data.refetch()
        },
        onMessage: (message) => {
            setWsMessages((prev) => [...(prev || []), message].slice(-250))
        },
    })

    const [autoScroll, setAutoScroll] = useState(true)
    const [wsMessages, setWsMessages] = useState<ChatMessage[]>([])
    useEffect(() => {
        if (autoScroll) scrollToBottom()
    }, [wsMessages, data.data])

    const messages = pageRecordsFlatten(data.data).reverse()
    const allMessages = [
        ...messages,
        ...wsMessages.filter(
            (wsMessage) =>
                !messages.some((message) => message.id === wsMessage.id)
        ),
    ]

    const scrollToBottom = () => {
        viewport.current?.scrollToIndex(allMessages.length - 1, {
            align: 'end',
        })
    }

    if (data.isLoading) return <PageLoader />
    if (!data.data && data.error) return <ErrorBox errorObj={data.error} />

    if (wsMessages?.length === 0 && messages.length === 0)
        return (
            <Flex
                justify="center"
                align="center"
                direction="column"
                gap="1rem"
                h="100%"
            >
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
                    messages={allMessages}
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
