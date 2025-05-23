import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Paper } from '@mantine/core'
import { ActivityFeedView } from './components/activity-feed-view'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Activity Feed - ${channel.display_name}`)

    return (
        <Paper
            h="calc(var(--tbot-content-height) + 1rem)"
            mt="-1rem"
            ml="-1rem"
            mr="-1rem"
        >
            <ActivityFeedView channelId={channel.id} />
        </Paper>
    )
}
