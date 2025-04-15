import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel/types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Box, Button } from '@mantine/core'
import { notifications } from '@mantine/notifications'
import { IconCheck } from '@tabler/icons-react'
import { useEffect, useRef, useState } from 'react'
import { VList, VListHandle } from 'virtua'
import { useGetChatlogs, useGetChatlogsWS } from '../api/chatlogs.api'
import { ChatMessage } from '../types/chat_message.type'
import { ChatMessages } from './chat-messages'

interface Props {
    channelId: ChannelId
}

export function ChatlogsViewer({ channelId }: Props) {
    const viewport = useRef<VListHandle>(null)
    const data = useGetChatlogs({
        channelId,
        params: {},
    })
    useEffect(() => {
        if (data.data) {
            setMessages(pageRecordsFlatten(data.data).reverse())
        }
    }, [data.data])

    useGetChatlogsWS({
        channelId,
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
        },
        onClose: (event) => {
            if (event.code === 1005) return
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
        },
        onMessage: (message) => {
            setMessages((prev) => [...prev, message].slice(-1000))
        },
    })

    const [autoScroll, setAutoScroll] = useState(true)
    const [messages, setMessages] = useState<ChatMessage[]>([])
    const scrollToBottom = () =>
        viewport.current?.scrollToIndex(messages.length - 1, {
            align: 'end',
        })
    useEffect(() => {
        if (autoScroll) scrollToBottom()
    }, [messages])

    if (data.isLoading) return <PageLoader />
    if (data.error) return <ErrorBox errorObj={data.error} />

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
                    <Button
                        onClick={() => {
                            data.fetchNextPage()
                        }}
                        variant="outline"
                        color="blue"
                        style={{
                            margin: '10px auto',
                            display: 'block',
                            width: 'fit-content',
                        }}
                    >
                        Load more
                    </Button>
                )}
                {data.isFetchingNextPage && <PageLoader />}
                <ChatMessages messages={messages} />
            </VList>

            {!autoScroll && (
                <Box
                    style={{
                        position: 'relative',
                    }}
                >
                    <Button
                        onClick={() => {
                            setAutoScroll(true)
                            scrollToBottom()
                        }}
                        style={{
                            position: 'absolute',
                            bottom: '50%',
                            left: '50%',
                        }}
                        variant="outline"
                        color="blue"
                    >
                        Resume chat
                    </Button>
                </Box>
            )}
        </>
    )
}
