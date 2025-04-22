import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import {
    ChatMessage,
    useGetChatlogs,
    useGetChatlogsWS,
} from '@/features/channel-combined-chat'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Flex, Text } from '@mantine/core'
import { IconNotification } from '@tabler/icons-react'
import { useEffect, useState } from 'react'
import { VList } from 'virtua'
import { NoticeFeedList } from './notice-feed-list'

interface Props {
    channelId: ChannelId
}

export function NoticeFeedViewer({ channelId }: Props) {
    const data = useGetChatlogs({
        channelId,
        params: {
            type: 'notice',
        },
    })
    useEffect(() => {
        if (data.data) {
            setNotices(pageRecordsFlatten(data.data))
        }
    }, [data.data])

    useGetChatlogsWS({
        channelId,
        connect: true,
        params: {
            type: 'notice',
        },
        onMessage: (message) => {
            setNotices((prev) => [...(prev || []), message].slice(-1000))
        },
    })

    const [notices, setNotices] = useState<ChatMessage[] | undefined>(undefined)

    if (data.isLoading || notices === undefined) return <PageLoader />
    if (data.error) return <ErrorBox errorObj={data.error} />

    if (notices.length === 0)
        return (
            <Flex
                justify="center"
                align="center"
                direction="column"
                gap="0.5rem"
                h="100%"
            >
                <IconNotification size={80} />
                <Text size="xl" fw={500}>
                    No notices
                </Text>
            </Flex>
        )
    return (
        <VList style={{ height: '100%' }}>
            <NoticeFeedList notices={notices || []} />
        </VList>
    )
}
