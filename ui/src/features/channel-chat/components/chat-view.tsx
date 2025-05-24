import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ViewerName } from '@/features/channel-viewer/types/viewer.type'
import { ChannelId } from '@/features/channel/types/channel.types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Flex, Text } from '@mantine/core'
import { IconMessage } from '@tabler/icons-react'
import { useEffect, useRef, useState } from 'react'
import { VList, VListHandle } from 'virtua'
import {
    GetChatMessageParams,
    useGetMessages,
    useWSChatMessages,
} from '../api/chat-messages.api'
import { ChatMessages } from './chat-messages'
import { LoadMoreButton } from './load-more-button'
import { ResumeChatButton } from './resume-chat-button'

interface Props {
    channelId: ChannelId
    liveUpdates?: boolean
    params?: GetChatMessageParams
    onViewerClick?: (viewer: ViewerName) => void
}

export function ChatView({
    channelId,
    liveUpdates,
    params,
    onViewerClick,
}: Props) {
    const viewport = useRef<VListHandle>(null)
    const [autoScroll, setAutoScroll] = useState(true)
    const data = useGetMessages({
        channelId,
        params,
    })
    useWSChatMessages({
        channelId,
        connect: liveUpdates,
        params,
    })

    const scrollToBottom = () => {
        viewport.current?.scrollToIndex(messages.length - 1, {
            align: 'end',
        })
    }

    useEffect(() => {
        if (autoScroll) scrollToBottom()
    }, [data.data])

    if (data.isLoading) return <PageLoader />
    if (!data.data && data.error) return <ErrorBox errorObj={data.error} />

    const messages = pageRecordsFlatten(data.data).reverse()

    if (messages.length === 0)
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
