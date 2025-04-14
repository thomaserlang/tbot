import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel/types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { ScrollArea } from '@mantine/core'
import { notifications } from '@mantine/notifications'
import { IconCheck } from '@tabler/icons-react'
import { useEffect, useRef, useState } from 'react'
import { useGetChatlogs, useGetChatlogsWS } from '../api/chatlogs.api'
import { ChatMessage } from '../types/chat_message.type'
import { ChatMessages } from './chat-messages'

interface Props {
    channelId: ChannelId
}

export function ChatlogsViewer({ channelId }: Props) {
    const viewport = useRef<HTMLDivElement>(null)
    const data = useGetChatlogs({
        channelId,
        params: {},
    })

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
            setMessages((prev) => [...prev, message].slice(-500))
        },
    })

    const [messages, setMessages] = useState<ChatMessage[]>([])

    const scrollToBottom = () =>
        viewport.current!.scrollTo({
            top: viewport.current!.scrollHeight,
            behavior: 'instant',
        })

    useEffect(() => {
        if (data.data) {
            setMessages(pageRecordsFlatten(data.data).reverse())
        }
    }, [data.data])

    useEffect(() => {
        if (viewport.current) scrollToBottom()
    }, [messages])

    if (data.isLoading) return <PageLoader />
    if (data.error) return <ErrorBox errorObj={data.error} />

    return (
        <ScrollArea
            onTopReached={() => {
                data.fetchNextPage()
            }}
            h="100%"
            type="hover"
            viewportRef={viewport}
        >
            {data.isFetchingNextPage && <PageLoader />}
            <ChatMessages messages={messages} />
        </ScrollArea>
    )
}
