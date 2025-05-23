import { ChannelId } from '@/features/channel'
import { Divider, Flex, Paper } from '@mantine/core'
import { ActivityFeedTable } from './activity-feed-table'
import { ActivityFeedHeader } from './activity-header'

interface Props {
    channelId: ChannelId
}

export function ActivityFeedView({ channelId }: Props) {
    return (
        <Flex
            direction="column"
            h="100%"
            w="100%"
            style={{ contain: 'strict' }}
        >
            <Paper>
                <Paper p="0.25rem 0.5rem">
                    <ActivityFeedHeader />
                </Paper>
                <Divider />
            </Paper>

            <ActivityFeedTable channelId={channelId} />
        </Flex>
    )
}
