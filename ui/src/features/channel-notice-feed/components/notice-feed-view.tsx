import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import {
    useGetChatlogs,
    useGetChatlogsWS,
} from '@/features/channel-combined-chat'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Divider, Flex, Paper, ScrollArea, Text } from '@mantine/core'
import { IconNotification } from '@tabler/icons-react'
import { NoticeFeedHeader } from './notice-feed-header'
import { NoticeFeedList } from './notice-feed-list'

interface Props {
    channelId: ChannelId
}

export function NoticeFeedView({ channelId }: Props) {
    const data = useGetChatlogs({
        channelId,
        params: {
            type: 'notice',
        },
    })

    useGetChatlogsWS({
        channelId,
        connect: true,
        params: {
            type: 'notice',
        },
    })

    if (data.isLoading) return <PageLoader />
    if (!data.data && data.error) return <ErrorBox errorObj={data.error} />

    const notices = pageRecordsFlatten(data.data)

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
        <Flex direction="column" h="100%" w="100%" gap="0.5rem">
            <Paper>
                <Paper p="0.25rem 0.5rem">
                    <NoticeFeedHeader />
                </Paper>
                <Divider />
            </Paper>
            <ScrollArea flex={1} style={{ contain: 'strict' }}>
                <NoticeFeedList notices={notices} />
            </ScrollArea>
        </Flex>
    )
}
